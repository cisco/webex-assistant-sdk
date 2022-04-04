class SimpleDialogueManager(DialogueManager):
    def add_rule(
        self, *, name: Optional[str] = None, pattern: Optional[str] = None, default=False, targeted_only=False
    ):
        """Wraps a function to behave as a dialogue handler"""

        # TODO: Take a closer look at the setup here, I'd like to have type hinting  # pylint:disable=fixme
        # catch if a function doesn't meet what's expected as a DialogueHandler
        # Just checking if handler is a coroutine is also an option
        def decorator(handler: DialogueHandler) -> DialogueHandler:
            if default:
                self.default_handler = handler
                return handler

            rule_name = name or handler.__name__.lower()
            if targeted_only:
                skill_rule = SimpleDialogueStateRule(None, rule_name)
                self.rules[skill_rule] = handler
            else:
                compiled = re.compile(pattern)
                skill_rule = SimpleDialogueStateRule(compiled, rule_name)
                self.rules[skill_rule] = handler

            return handler

        return decorator