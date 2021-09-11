from typing import GenericAlias
from datetime import datetime, date, time

from .field import Field
from .listfield import ListField
from .typefield import TypeField
from .sectionfield import SectionField
from .missing import MISSING
from .util import get_attr_typevals
from .exceptions import MissingAnnotationException, InvalidFieldTypeException


class Config:
    __nconf_root__: SectionField

    def __new__(cls, dataval=None):
        if dataval is None:
            return object.__new__(cls)
        path = cls.__name__
        obj = cls.__nconf_root__.parse(dataval, path)
        return obj

    def __repr__(self):
        field_names = self.__class__.__nconf_root__.subfields.keys()
        field_vals = ((name, val) for name, val in self.__dict__.items() if name in field_names)
        attr_strs = (f"{name}={val!r}" for name, val in field_vals)
        attrs = ", ".join(attr_strs)
        return f"{self.__class__.__name__}({attrs})"


def _config(cls: type) -> type[Config]:
    cls: type[Config] = type(cls.__name__, (Config, ), dict(cls.__dict__))
    path = cls.__name__
    fields = get_class_fields(cls, path)
    cls.__nconf_root__ = SectionField(cls, fields)
    return cls


def config(cls=None):
    def wrap(cls):
        return _config(cls)

    # We're called as @config() with parens.
    if cls is None:
        return wrap

    # We're called as @config without parens.
    return wrap(cls)


def _section(cls):
    cls.__nconf_section__ = True
    return cls


def section(cls=None):
    def wrap(cls):
        return _section(cls)

    # We're called as @section() with parens.
    if cls is None:
        return wrap

    # We're called as @section without parens.
    return wrap(cls)


def get_class_fields(cls: type, path: str) -> dict[str, Field]:
    """Get all fields"""
    return {name: get_field(typ, val, f"{path}.{name}") for name, (typ, val) in get_attr_typevals(cls).items()}


def get_field(typ, val, path: str) -> Field:
    """Parse a type/value and return a Field"""
    # manually entered Field entry
    if _is_field(val):
        return val

    f = get_typefield(typ, val, path) or get_listfield(typ, val, path) or get_sectionfield(typ, val, path)

    if f is None:
        if typ is MISSING:
            raise MissingAnnotationException
        field_type_name = getattr(typ, '__name__', repr(typ))
        raise InvalidFieldTypeException(f"Invalid field type {field_type_name} in path {path}")

    return f


def get_listfield(typ, val, path: str):
    """Parse a type/value and return a ListField if possible, otherwise return None"""
    subpath = f"{path}[]"
    typ = _normalize_list_type(typ)
    if not _is_list(typ):
        return
    subfield: Field = get_field(typ.__args__[0], MISSING, subpath)
    return ListField(typ, subfield, default=val)


def get_typefield(typ, val, path: str):
    """Parse a type/value and return a TypeField if possible, otherwise return None"""
    if typ not in (str, int, float, bool, datetime, date, time):
        return
    return TypeField(typ, default=val)


def get_sectionfield(typ, val, path: str):
    """Parse a type/value and return a SectionField if possible, otherwise return None"""
    if _is_section(val) and typ is MISSING:
        cls = val
    elif _is_section(typ) and val is MISSING:
        cls = typ
    else:
        return
    fields = get_class_fields(cls, path)
    return SectionField(cls, fields)


def _is_section(cls):
    return isinstance(cls, type) and getattr(cls, "__nconf_section__", False)


def _is_list(typ):
    return isinstance(typ, GenericAlias) and typ.__origin__ is list


def _is_field(obj):
    return isinstance(obj, Field)


def _normalize_list_type(typ):
    if typ is list:
        return list[str]
    elif _is_list(typ):
        return list[_normalize_list_type(typ.__args__[0])]
    return typ
