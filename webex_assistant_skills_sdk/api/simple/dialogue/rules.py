class SimpleDialogueStateRule:
    def __init__(self, regex: Optional[re.Pattern], dialogue_state: str):
        self.regex = regex
        self.dialogue_state = dialogue_state

    def match(self, text) -> Optional[re.Match]:
        if not self.regex:
            return None
        return self.regex.match(text)
