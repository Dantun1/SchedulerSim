from enum import Enum, auto

class ProcessState(Enum):
    RUNNING = auto()
    READY = auto()
    BLOCKED = auto()
    NEW = auto()
    TERMINATED = auto()

class ProcessAction(Enum):
    RUN = auto()
    ISSUE_IO = auto()
    TERMINATE = auto()

# class OSCosts(Enum):
#     CONTEXT_SWITCH = 1
#