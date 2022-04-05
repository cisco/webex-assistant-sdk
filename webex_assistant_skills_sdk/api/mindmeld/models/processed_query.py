from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class ProcessedQuery(BaseModel):
    # This is a subset of the fields on ProcessedQuery. We will only ever receive a single transcript
    # So we don't need to include any of the nbest_* fields or the confidence
    text: str
    domain: Optional[str]
    intent: Optional[str]
    # TODO: Add proper typing for entities (dict with keys for entity types and values)   # pylint:disable=fixme
    entities: Optional[List[Dict[str, Any]]] = []
