from logging import getLogger
from threading import Thread
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

    #task->execute
    def execute(self, name: str, workflow: Workflow) -> None:
        task_name = self.name + "." + name
        if isinstance(workflow, Task):
            LOG.info(f"{task_name} Entry")
            func = FunctionFactory.get_function(workflow.function)
            self.data[task_name] = func.execute(task_name, workflow.inputs)
            LOG.info(f"{task_name} Exit")

        elif isinstance(workflow, Flow):
            executor = Executor(task_name, workflow, self.data)
            executor.start_execution()

    #flow->excute
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
