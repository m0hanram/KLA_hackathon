from models.workflow import Workflow
from models.workflow import Workflow
import functions
from concurrent.futures import ThreadPoolExecutor


def execute_function(object: Workflow):
    if object.workflow_type=="Task":
        if object.function == "TimeFunction":
            pass

    if object.workflow_type == "Flow":
        if object.execution == "Sequential":
            for activity in object.activities:
                execute_function(activity)
        else:
            with ThreadPoolExecutor(max_workers=len(object.activities)) as executer:
                executer.map(execute_function, range(len(object.activities)), object.activities)

