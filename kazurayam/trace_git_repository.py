from abc import ABCMeta, abstractmethod
from enum import IntEnum, auto


class GitRepositoryVisitResult(IntEnum):
    CONTINUE = auto()
    SKIP_SIBLINGS = auto()
    SKIP_SUBTREE = auto()
    TERMINATE = auto()


class TraceMain:
    pass

