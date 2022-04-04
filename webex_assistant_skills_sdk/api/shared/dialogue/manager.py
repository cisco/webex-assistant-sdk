class DialogueManager:
    def __init__(self, rules: Optional[RuleMap] = None, default_handler: Optional[DialogueHandler] = None):
        self.rules = rules or {}
        self.default_handler = default_handler

    def get_handler(self, query: DialogueQuery, target_state: Optional[str] = None) -> Optional[DialogueHandler]:
        for rule, handler in self.rules.items():
            if target_state and rule.dialogue_state == target_state:
                return handler
            if not target_state and rule.match(query):
                return handler
        return None

    async def handle(self, query: DialogueQuery, current_state: DialogueState):
        # Iterate over our rules, taking the first match
        handler = self.get_handler(query, current_state.params.target_dialogue_state)
        handler = handler or self.default_handler

        if not handler:
            # TODO: Different message  # pylint:disable=fixme
            raise MissingHandler('No handler found')

        # TODO: Use annotated types rather than length  # pylint:disable=fixme
        handler_args = inspect.signature(handler)
        if len(handler_args.parameters) == 2:
            new_state = await handler(current_state, query)
        else:
            new_state = await handler(current_state)
        new_state.update_history(old_state=current_state)
        return new_state
