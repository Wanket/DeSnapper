from typing import Callable, TypeVar, Generic, Set

FunctionType = TypeVar("FunctionType")


class BaseHandler(Generic[FunctionType]):
    def __init__(self):
        self.__callbacks: Set[FunctionType] = set()

    def __iadd__(self, callback: FunctionType):
        self.__callbacks.add(callback)

    def __isub__(self, callback: FunctionType):
        self.__callbacks.remove(callback)

    def emit(self, *args, **kwargs):
        for callback in self.__callbacks:
            callback(args, kwargs)
