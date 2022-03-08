from enum import Enum


class WorkflowType(str, Enum):
    Task = "Task"
    Flow = "Flow"


class ExecutionType(str, Enum):
    Sequential = "Sequential"
    Concurrent = "Concurrent"


class FunctionType(str, Enum):
    Binning = "Binning"
    DataLoad = "DataLoad"
    TimeFunction = "TimeFunction"
    MergeResults = "MergeResults"
    ExportResults = "ExportResults"
