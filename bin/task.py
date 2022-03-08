from . import framework
import time 

class Task(framework.WorkFlow):
    def __init__(self, name: str, function: str, inputs: dict, outputs: list[str], condition: str) -> None:
        super().__init__(name)
        self.function = function
        self.inputs = inputs
        self.outputs = outputs
        self.condition = condition
    
    def execute(self):
        if self.function == 'TimeFunction':
            time.sleep(self.inputs['ExecutionTime'])
            