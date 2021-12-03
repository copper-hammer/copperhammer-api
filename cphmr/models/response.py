from typing import Optional

from pydantic import BaseModel

from cphmr.scanner.exceptions.errors import ErrorBase as ScannerErrorBase


class MainResponseBase(BaseModel):
    """
    Base model for all responses.
    """

    action: str = "ACTION"
    result: Optional[dict] = None
    error: ScannerErrorBase

    class Config:  # skipcq: PY-D0002
        use_enum_values = True
