from datetime import timedelta
from ipaddress import IPv4Address
from typing import Union

from pydantic import BaseModel
from pydantic.class_validators import validator
from pydantic.types import UUID4, NonNegativeFloat, NonNegativeInt, PositiveInt

from cphmr.scanner.typesa import ActionTypes

# MARK: - Request models for HTTP's AUTHENTICATE_REQUEST


class AuthenticationRequest(BaseModel):
    """
    Request model for authentication of a scanner node.
    """

    action: ActionTypes

    class Config:  # skipcq: PY-D0002
        use_enum_values = True


# MARK: - Request models for YAGOOD_NODE


class YagoodNodeRequest(BaseModel):
    """
    Request model for YAGOOD request.
    """

    ok: bool


# MARK: - Request models for REQUEST_BATCH


class RequestBatchRequest(BaseModel):
    """
    Request model for batch processing of requests.
    """

    workers: PositiveInt


# MARK: - Request models for BATCH_ACCEPT_CONFIRM


class BatchInfoSus(BaseModel):
    """
    Model for batch information.
    """

    batchID: UUID4
    serverIP: IPv4Address


class BatchAcceptConfirmRequest(BaseModel):
    """
    Request model for confirming a batch of requests.
    """

    batchInfo: BatchInfoSus


# MARK: - Request models for SUBMIT_RESULTS


class VersionInfomationServerInfo(BaseModel):
    """
    Model for version information of a server.
    """

    name: str
    protocol: int
    is_modded: bool
    mods: list[str]


class SinglePlayerInformation(BaseModel):
    """
    Model for single player information.
    """

    uuid: UUID4
    name: str


class PlayerInfomationServerInfo(BaseModel):
    """
    Model for player information of a server.
    """

    online: NonNegativeInt
    max: NonNegativeInt
    sample: list[SinglePlayerInformation]


class CompletedServerInfo(BaseModel):
    """
    Model for completed server information.
    """

    host: IPv4Address
    port: NonNegativeInt
    title: str
    version: VersionInfomationServerInfo
    players: PlayerInfomationServerInfo


class StatsSubmittedServers(BaseModel):
    """
    Stats about completed batch.
    """

    duration: timedelta


class SubmitResultsRequest(BaseModel):
    """
    Request model for submitting results.
    """

    batchID: UUID4
    results: list[CompletedServerInfo]
    stats: StatsSubmittedServers


# MARK: - BASEd request model

def getResultSheesh(
    result: dict, action: ActionTypes) -> Union[AuthenticationRequest,
                                                YagoodNodeRequest,
                                                RequestBatchRequest,
                                                BatchAcceptConfirmRequest,
                                                SubmitResultsRequest]:
    """
    Get the result's corresponding model of a request.
    """
    match action:
        case "YAGOOD_NODE":
            return YagoodNodeRequest(**result)
        case "REQUEST_BATCH":
            return RequestBatchRequest(**result)
        case "BATCH_ACCEPT_CONFIRM":
            return BatchAcceptConfirmRequest(**result)
        case "SUBMIT_RESULTS":
            return SubmitResultsRequest(**result)


class WebSocketMessageRequest(BaseModel):
    """
    Request model for receiving messages from a scanner node.
    """

    action: ActionTypes
    result: dict

    @validator("result", always=True)
    def validateResultField(cls, value, values):  # skipcq: PYL-R0201
        """
        Validate the result field.
        """
        return getResultSheesh(value, values["action"])

    class Config:  # skipcq: PY-D0002
        use_enum_values = True
