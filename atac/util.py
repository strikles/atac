import regex
import unicodedata
from pydbg import *


def breakpoint_handler(dbg):
   print(dbg.dump_context())
   return DBG_CONTINUE


# Defining a decorator
def inspect(f):
    def wrap(*args, **kwargs):
        dbg(f(*args, **kwargs))
        return f(*args, **kwargs)

    return wrap


# Defining a decorator
def trace(f):
    def wrap(*args, **kwargs):
        print(f"[TRACE] func: {f.__name__}, args: {args}, kwargs: {kwargs}")
        return f(*args, **kwargs)

    return wrap


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    try:
        raise TypeError()
    except (ValueError, TypeError) as exception:
        print("Catching all exceptions")


def remove_accent_chars_regex(x: str):
    return regex.sub(r'\p{Mn}', '', unicodedata.normalize('NFKD', x))


def remove_accent_chars_join(x: str):
    # answer by MiniQuark
    # https://stackoverflow.com/a/517974/7966259
    return u"".join([c for c in unicodedata.normalize('NFKD', x) if not unicodedata.combining(c)])