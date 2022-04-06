class MindmeldDialogueManager(DialogueManager):
    def add_rule(
        self,
        *,
        name: Optional[str] = None,
        default=False,
        domain=None,
        intent=None,
        entities=None,
        targeted_only=False,
    ):
        """Wraps a function to behave as a dialogue handler"""

        def decorator(handler: DialogueHandler) -> DialogueHandler:
            if default:
                self.default_handler = handler
                return handler

            rule_name = name or handler.__name__.lower()
            skill_rule = MMDialogueStateRule(domain, intent, entities, rule_name, targeted_only=targeted_only)
            self.rules[skill_rule] = handler
            existing_rules: List[(MMDialogueStateRule, DialogueHandler)] = list(self.rules.items())
            self.rules = dict(sorted(existing_rules, reverse=True))

            return handler

        return decorator
    