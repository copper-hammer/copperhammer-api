from typing import Optional, TypedDict

from pydantic import BaseModel
from pydantic.types import UUID4

from cphmr.scanner.exceptions.errors import ErrorBase
from cphmr.scanner.typesa import ActionTypes


class AuthorizedStatusForResponse(TypedDict):
    """
    A TypedDict for the authorized status for a response.

    Just a simple 'wrapper' around a boolean.
    """

    succcess: bool


class NodeInfoForResponse(TypedDict):
    """
    A TypedDict for the node info for a response. Used in a `node_register` response.

    nodeID is a UUID4, and the nodeToken is a string containing the token\
    (should be 128 bits).
    """

    nodeID: UUID4
    nodeToken: str


class AuthenticationResponse(TypedDict):
    """
    Model for the authentication response from a scanner node.
    """

    authorization: AuthorizedStatusForResponse
    nodeInfo: NodeInfoForResponse


class ResponseBase(BaseModel):
    """
    Base model for all responses.
    """

    action: ActionTypes
    result: Optional[AuthenticationResponse] = None
    error: Optional[ErrorBase] = None

    class Config:  # skipcq: PY-D0002
        use_enum_values = True
