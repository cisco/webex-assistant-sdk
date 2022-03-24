from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class InvokePayloadEncrypted(BaseModel):
    signature: str
    message: str


class InvokeResponse(BaseModel):
    challenge: str
    directives: List[Dict[Any, Any]]
    frame: Optional[Dict[Any, Any]] = []
    params: Optional[Params] = {}
    history: Optional[List[Dict[Any, Any]]] = []
