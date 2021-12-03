from pydantic import BaseModel

from cphmr.scanner.typesa import ErrorTypes


class ErrorBase(BaseModel):
    """
    Error base model
    """

    name: ErrorTypes
    description: str

    class Config:  # skipcq: PY-D0002
        use_enum_values = True
