from concurrent.futures import ThreadPoolExecutor
from logging import getLogger
from typing import Optional

from functions import FunctionFactory
from models.enums import ExecutionType
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

    def execute(self, name: str, workflow: Workflow) -> None:
        task_name = self.name + "." + name
        LOG.info(f"{task_name} Entry")
        if isinstance(workflow, Task):
            func = FunctionFactory.get_function(workflow.function)
            self.data[task_name] = func.execute(task_name, workflow.inputs)
        elif isinstance(workflow, Flow):
            executor = Executor(task_name, workflow, self.data)
            executor.start_execution()
        LOG.info(f"{task_name} Exit")

    def start_execution(self) -> dict:
        LOG.info(f"{self.name} Entry")

        if self.flow.execution == ExecutionType.Sequential:
            for name, workflow in self.flow.activities.items():
                self.execute(name, workflow)
        elif self.flow.execution == ExecutionType.Concurrent:
            with ThreadPoolExecutor(max_workers=len(self.flow.activities)) as executor:
                executor.map(self.execute, self.flow.activities.items())

        LOG.info(f"{self.name} Exit")
        return self.data
