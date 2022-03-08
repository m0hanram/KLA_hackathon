import time
from abc import ABC
from logging import getLogger
from typing import Any

import pandas as pd

from models.enums import FunctionType
from models.inputs import DataLoadInput, Input, TimeFunctionInput
from models.workflow import Task

LOG = getLogger()


class FunctionContract(ABC):
    @staticmethod
    def execute(task_name: str, func_input: Input) -> Any:
        ...


class TimeFunction(FunctionContract):
    @staticmethod
    def execute(task_name: str, func_input: TimeFunctionInput) -> None:
        LOG.info(
            f"{task_name} Executing TimeFunction ({func_input.function_input}, {func_input.execution_time})"
        )
        time.sleep(func_input.execution_time)


class DataLoadFunction(FunctionContract):
    @staticmethod
    def execute(task_name: str, func_input: DataLoadInput) -> None:
        LOG.info(f"{task_name} Executing DataLoad ({func_input.filename})")
        return pd.read_csv(func_input.filename)


class FunctionFactory:
    function_map = {
        FunctionType.DataLoad: DataLoadFunction,
        FunctionType.TimeFunction: TimeFunction,
    }

    @classmethod
    def get_function(cls, func_type: FunctionType) -> FunctionContract:
        return cls.function_map[func_type]
