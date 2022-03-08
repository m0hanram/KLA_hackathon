from . import framework 

class Flow(framework.WorkFlow):
    def __init__(self, name: str, execution: str, activities: framework.WorkFlow = None) -> None:
        super().__init__(name, 'flow')
        self.execution = execution
        self.activies = activities

    def execute(self):
        if self.execution=='Sequential':
            for activity in self.activities:
                activity.execute()
            
