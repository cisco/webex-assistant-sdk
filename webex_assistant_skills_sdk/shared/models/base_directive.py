from typing import Any, Dict, Optional
from pydantic import BaseModel


class Directive(BaseModel):
    name: str
    payload: Optional[Dict[str, Any]]
