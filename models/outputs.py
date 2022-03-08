from enum import Enum

from pydantic import BaseModel, Field

from models.enums import FunctionType


class Output(str, Enum):
    DataTable = "DataTable"
    NoOfDefects = "NoOfDefects"
    MergedResults = "MergedResults"
    BinningResultsTable = "BinningResultsTable"


OUTPUT_MAPPING = {
    FunctionType.DataLoad: [Output.NoOfDefects, Output.DataTable],
    FunctionType.MergeResults: [Output.NoOfDefects, Output.MergedResults],
    FunctionType.Binning: [Output.MergedResults, Output.BinningResultsTable],
}
