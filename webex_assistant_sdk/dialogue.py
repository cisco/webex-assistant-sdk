import uuid

from mindmeld.components.dialogue import DialogueResponder, DirectiveNames


class AssistantDirectiveNames(DirectiveNames):
    """A constants object for directive names."""

    DISPLAY_WEB_VIEW = 'display-web-view'
    """A directive to display a web view."""

    CLEAR_WEB_VIEW = 'clear-web-view'
    """A directive to clear a web view"""

    UI_HINT = 'ui-hint'
    """A directive to display a UI hint."""

    ASR_HINT = 'asr-hint'
    """A directive to display an ASR hint."""

    LONG_REPLY = 'long-reply'
    """A directive to display long replies."""

    DISPLAY = 'display'
    """A generic display directive."""

    ASSISTANT_EVENT = 'assistant-event'
    """A directive to forward a generic payload"""


class DirectiveNotSupportedError(Exception):
    pass


class DirectiveFormatError(Exception):
    pass


class SkillResponder(DialogueResponder):
    DirectiveNames = AssistantDirectiveNames
    group_counter = 0

    def direct(self, name, dtype, payload=None, did=None):  # pylint: disable=arguments-differ
        """Adds an arbitrary directive and return it.

        Args:
            name (str): The name of the directive.
            dtype (str): The type of the directive.
            payload (dict, optional): The payload for the directive.
            did (str): Directive id, for logging purpose.

        Returns:
            (dict): Added directive.
        """
        if not self.is_directive_supported(name):
            raise DirectiveNotSupportedError

        directive = {'name': name, 'type': dtype}

        if payload:
            directive['payload'] = payload

        if did:
            directive['id'] = did

        self.directives.append(directive)
        return directive

    def speak(self, text, remove_hyphens=False):  # pylint: disable=arguments-differ
        """Adds a 'speak' directive.

        Args:
            text (str): The text to speak aloud.
            remove_hyphens (bool): Should hyphens in the text be removed.
        """
        text = self._process_template(text)
        if remove_hyphens:
            text = text.replace('-', ' ')
        self.act(self.DirectiveNames.SPEAK, payload={'text': text})

    def display(self, name, payload=None):
        """Adds an arbitrary directive of type 'view' and return it.

        Args:
            name (str): The name of the directive.
            payload (dict, optional): The payload for the view.

        Returns:
            (dict): added directive of type view.
        """
        return self.direct(name, self.DirectiveTypes.VIEW, payload=payload, did=str(uuid.uuid4()))

    def display_web_view(self, url=None):
        """Displays a web view.

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
            templates (list): The list of hint templates.
            prompt (string): An optional prompt to precede the hints.
            display_immediately (boolean): Show hints as soon as possible?
        """
        texts = []
        for template in templates:
            template = self._choose(template)
            texts.append(template.format(**self.slots))

        payload = {'text': texts}
        if prompt:
            payload['prompt'] = prompt
        if display_immediately:
            payload['displayImmediately'] = True
        self.display(self.DirectiveNames.UI_HINT, payload=payload)

    def asr_hints(self, templates):
        """Sends asr hints which helps the ASR to recognize better.

        Args:
            templates (list): The list of ASR templates/texts.
        """
        texts = []
        for template in templates:
            template = self._choose(template)
            texts.append(template.format(**self.slots))
        payload = {'text': texts}
        self.act(self.DirectiveNames.ASR_HINT, payload=payload)

    def clear_web_view(self):
        """Dismisses the web view."""
        self.act(self.DirectiveNames.CLEAR_WEB_VIEW)

    def reply(  # pylint: disable=arguments-differ
        self, response_strings, increment_group=False, is_spoken=True, remove_hyphens=False
    ):
        """Sends a 'reply' view and a 'speak' directive.

        Args:
            response_strings (ResponseStrings): A list of reply templates.
            increment_group (bool): Should text belong to next group.
            is_spoken (bool): Should the text be spoken.
            remove_hyphens (bool): Should hyphens in the text be removed in speak directives.
        """
        template = self._choose(response_strings)
        text = template.format(**self.slots)

        # Send reply
        success = self._reply(text, increment_group=increment_group)

        if is_spoken:
            try:
                self.speak(text=text, remove_hyphens=remove_hyphens)
                success = True
            except DirectiveNotSupportedError:
                pass

        # If we sent neither reply or speak, raise error
        if not success:
            raise DirectiveNotSupportedError

    def _reply(self, text, increment_group=False):
        """Sends a 'reply' view directive.

        Args:
            text (str): Reply that should be displayed.
            increment_group (bool, optional): Should text belong to next group.

        Returns:
            (bool): If the 'reply' view was successfully added
        """
        if increment_group:
            self.group_counter += 1

        if self.group_counter > 2:
            raise DirectiveFormatError('reply directive can only support two groups.')

        payload = {'text': text, 'group': self.group_counter}
        success = False
        try:
            self.display(self.DirectiveNames.REPLY, payload=payload)
            success = True
        except DirectiveNotSupportedError:
            pass

        return success

    def long_reply(
        self, response_strings: list, is_spoken: bool = True, remove_hyphens: bool = False
    ):
        """Sends a 'long-reply' view and a 'speak' directive. Used for replies
        are too long to be sent as a normal 'reply' and which should be
        formatted appropriately.

        Args:
            response_strings (list): A list of reply templates.
            is_spoken (bool): Should the text be spoken.
            remove_hyphens (bool): Should hyphens in the text be removed in speak directives.
        """
        template = self._choose(response_strings)
        text = template.format(**self.slots)
        payload = {'text': text}
        success = False

        try:
            self.display(self.DirectiveNames.LONG_REPLY, payload=payload)
            success = True
        except DirectiveNotSupportedError:
            # Note: should we use a normal reply in these cases?
            pass

        if is_spoken:
            try:
                self.speak(text=text, remove_hyphens=remove_hyphens)
                success = True
            except DirectiveNotSupportedError:
                pass

        # If we sent neither long reply or speak, raise error.
        if not success:
            raise DirectiveNotSupportedError

    def send_assistant_event(self, name, payload=None):
        """Sends a 'assistant-event' directive

        Args:
            name (string): Used to identify the source of the event
            payload (json object, optional): Payload to forward
        """
        self.act(self.DirectiveNames.ASSISTANT_EVENT, {
            'name': name,
            'payload': payload,
        })

    @property
    def supported_directives(self):
        return [
            getattr(self.DirectiveNames, at)
            for at in dir(self.DirectiveNames)
            if not at.startswith('__')
        ]

    def is_directive_supported(self, directive):
        return directive in self.supported_directives
