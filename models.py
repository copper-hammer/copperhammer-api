# from dataclasses import dataclass
# from typing import Union

from pydantic import BaseModel


class ScannerNodeRegistration(BaseModel):
    """
    Scanner node registration model input request.
    """

    action: str
