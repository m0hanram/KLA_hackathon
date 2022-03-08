import re
from logging import getLogger
from threading import Thread
from typing import Any, Optional
from xmlrpc.client import Boolean

from functions import FunctionFactory
from models.enums import ExecutionType
from models.inputs import Input
from models.workflow import Flow, Task, Workflow

LOG = getLogger()


class Executor:
    def __init__(self, name: str, flow: Flow, data: Optional[dict] = None):
        self.name = name
        self.flow = flow
        if data:
            self.data = data
        else:
            self.data = {}

    def get_replaced_value(self, val):
        reference_match = re.match(r"^\$\(([A-Za-z.0-9]+)\)", val)
        if reference_match:
            key_with_filed = reference_match.group(1)
            last_dot = key_with_filed.rfind(".")
            key, field = key_with_filed[:last_dot], key_with_filed[last_dot + 1 :]
            vals = self.data[self.name + "." + key]
            val = vals[field]
        return val

    def replace_inputs(self, inputs: Input) -> Input:
        replaced = inputs.dict(by_alias=True)
        for name, value in replaced.items():
            if not value:
                continue
            if isinstance(value, str):
                replaced[name] = self.get_replaced_value(value)

        return inputs.__class__(**replaced)

    def check_condition(self, condition: str) -> Boolean:
        if ")" in condition:
            replacement = self.get_replaced_value(condition)
            end_index = condition.find(")")
            condition = str(replacement) + condition[end_index + 1 :]
            condition = condition.replace(" ", '')
        result = eval(condition)
        return bool(result)

    def execute(self, name: str, workflow: Workflow) -> None:
        task_name = self.name + "." + name
        if isinstance(workflow, Task):
            LOG.info(f"{task_name} Entry")
            if workflow.condition is None or self.check_condition(workflow.condition):
                inputs = self.replace_inputs(workflow.inputs)
                func = FunctionFactory.get_function(workflow.function)
                self.data[task_name] = func.execute(task_name, inputs)
            else:
                LOG.info(f"{task_name} Skipped")

            LOG.info(f"{task_name} Exit")

        elif isinstance(workflow, Flow):
            executor = Executor(task_name, workflow, self.data)
            executor.start_execution()

    def start_execution(self) -> dict:
        LOG.info(f"{self.name} Entry")

        if self.flow.execution == ExecutionType.Sequential:
            for name, workflow in self.flow.activities.items():
                self.execute(name, workflow)

        elif self.flow.execution == ExecutionType.Concurrent:
            threads = []
            for name, workflow in self.flow.activities.items():
                th = Thread(target=self.execute, args=(name, workflow))
                threads.append(th)
            [th.start() for th in threads]
            [th.join() for th in threads]

        LOG.info(f"{self.name} Exit")
        return self.data
