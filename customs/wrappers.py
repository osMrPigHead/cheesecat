"""一些用得比较多的装饰器"""
__all__ = [
    "decompose_first_tuple_f", "decompose_first_tuple_m",
    "ensure_type", "ensure_ndarray",
    "iterator2list"
]

import functools

import numpy as np


def decompose_first_tuple_f(func):
    """将函数的参数首项元组解开"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) != 1:
            return func(*args, **kwargs)
        return func(*args[0])
    return wrapper


def decompose_first_tuple_m(func):
    """将方法的参数首项元组解开"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) != 2:
            return func(*args, **kwargs)
        return func(args[0], *args[1])
    return wrapper


def ensure_type(type_=type, *argi: int | str, builder=None):
    """确保指定的参数类型"""
    if builder is None:
        builder = type_
    ints, strs = [], []
    for arg in argi:
        if isinstance(arg, int):
            ints += [arg]
        if isinstance(arg, str):
            strs += [arg]

    def _ensure_type(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args = list(args)
            for i in ints:
                if len(args) > i and not isinstance(args[i], type_):
                    args[i] = builder(args[i])
            for i in strs:
                if i in kwargs and not isinstance(kwargs[i], type_):
                    kwargs[i] = builder(kwargs[i])
            return func(*args, **kwargs)
        return wrapper

    return _ensure_type


def ensure_ndarray(*argi: int | str, builder=np.stack):
    """确保指定的参数为 ndarray"""
    return ensure_type(np.ndarray, *argi, builder=builder)


def iterator2list(*out: int):
    """将输出转换成 list"""
    def _iterator2list(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            main = list(func(*args, **kwargs))
            other = []
            for i in out:
                other += [main[i]]
                del main[i]
            return main, *other
        return wrapper
    return _iterator2list
