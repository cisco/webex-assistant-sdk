from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar('T')

class DialogueRule(BaseModel, Generic[T]):
    dialogue_state: str

    def match(self, _: T) -> bool:
        '''Override in subclass'''
