from __future__ import annotations

from abc import ABC

from pydantic import BaseModel, Field, root_validator

from models.enums import ExecutionType, FunctionType, WorkflowType
from models.inputs import INPUT_MAPPING, Input
from models.outputs import OUTPUT_MAPPING, Output


class Workflow(ABC, BaseModel):
    workflow_type: WorkflowType = Field(alias="Type")


class Task(Workflow):
    function: FunctionType = Field(alias="Function")
    inputs: Input = Field(alias="Inputs")
    outputs: list[Output] = Field(alias="Outputs", default=None)
    condition: str = Field(alias="Condition", default=None)

    @root_validator(pre=True)
    def _set_fields(cls, values: dict) -> dict:
        func_type = FunctionType[values["Function"]]
        values["Inputs"] = INPUT_MAPPING[func_type](**values["Inputs"])
        if values.get("Outputs"):
            outputs = []
            for output in values["Outputs"]:
                if output in OUTPUT_MAPPING[func_type]:
                    outputs.append(Output[output])
                else:
                    raise Exception("Invalid Output field")
            values["Outputs"] = outputs

        return values


class Flow(Workflow):
    execution: ExecutionType = Field(alias="Execution")
    activities: dict[str, Workflow] = Field(alias="Activities")

    @root_validator(pre=True)
    def _set_fields(cls, values: dict) -> dict:
        activities = {}
        for name, vals in values["Activities"].items():
            workflow_type = WorkflowType[vals["Type"]]
            if workflow_type == WorkflowType.Flow:
                activities[name] = cls(**vals)
            else:
                activities[name] = Task(**vals)
        values["Activities"] = activities
        return values
