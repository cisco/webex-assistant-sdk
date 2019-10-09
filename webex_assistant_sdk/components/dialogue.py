from mindmeld.components.dialogue import DirectiveNames, DialogueResponder


class AssistantDirectiveNames(DirectiveNames):
    """A constants object for directive names."""

    DISPLAY_WEB_VIEW = 'display-web-view'
    """A directive to display a web view."""

    UI_HINT = 'ui-hint'
    """A directive to display a UI hint."""

    ASR_HINT = 'asr-hint'
    """A directive to display an ASR hint."""

    GO_HOME = 'go-home'
    """A directive to dismiss the web view."""


class AssistantDialogueResponder(DialogueResponder):
    DirectiveNames = AssistantDirectiveNames

    def display_web_view(self, url=None):
        """Displays a web view

        Args:
            url (str): The url of the web view
        """
        if url:
            self.act(self.DirectiveNames.DISPLAY_WEB_VIEW, payload={'url': url})
        else:
            self._logger.warning('No url is passed for display web view directive.')

    def ui_hints(self, templates, prompt=None, display_immediately=False):
        """Sends a 'hint' view'

        Args:
            templates (list): The list of hint templates
            prompt (string): An optional prompt to precede the hints
            display_immediately (boolean): Show hints as soon as possible?
        """
        texts = []
        for template in templates:
            template = self._choose(template)  # pylint: disable=no-member
            texts.append(template.format(**self.slots))

        payload = {'text': texts}
        if prompt:
            payload['prompt'] = prompt
        if display_immediately:
            payload['displayImmediately'] = True
        self.display(self.Directives.UI_HINT, payload=payload)

    def asr_hints(self, templates):
        """Sends asr hints which helps the ASR to recognize better.

        Args:
            templates (list): The list of ASR templates/texts.
        """
        texts = []
        for template in templates:
            template = self._choose(template)  # pylint: disable=no-member
            texts.append(template.format(**self.slots))
        payload = {'text': texts}
        self.act(self.Directives.ASR_HINT, payload=payload)  # pylint: disable=no-member

    def go_home(self):
        """Dismisses the web view."""
        self.act(self.DirectiveNames.GO_HOME)