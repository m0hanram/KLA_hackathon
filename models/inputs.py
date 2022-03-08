from pydantic import BaseModel, Field

from models.enums import FunctionType


class Input(BaseModel):
    ...


class BinningInput(Input):
    rule_filename: str = Field(alias="RuleFilename")
    data_set_1: str = Field(alias="DataSet1")


class DataLoadInput(Input):
    filename: str = Field(alias="Filename")


class TimeFunctionInput(Input):
    function_input: str = Field(alias="FunctionInput")
    execution_time: int = Field(alias="ExecutionTime")


class MergeResultsInput(Input):
    precedence_file: str = Field(alias="PrecedenceFile")
    data_set_1: str = Field(alias="DataSet1")
    data_set_2: str = Field(alias="DataSet2")


class ExportResultsInput(Input):
    file_name: str = Field(alias="FileName")
    defect_table: str = Field(alias="DefectTable")


INPUT_MAPPING = {
    FunctionType.Binning: BinningInput,
    FunctionType.DataLoad: DataLoadInput,
    FunctionType.TimeFunction: TimeFunctionInput,
    FunctionType.MergeResults: MergeResultsInput,
    FunctionType.ExportResults: ExportResultsInput,
}
