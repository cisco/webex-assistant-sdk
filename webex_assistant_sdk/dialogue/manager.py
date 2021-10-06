class DialogueManager:
    def handle(self):
        # TODO: Cast request/responder objects
        request = self.request_class(processed_query)
        responder = self.responder_class(frame=invoke_request.frame)  # Additional arguments to initialize responder
        # TODO: Run dialogue manager apply handler method
        # This just mutates and returns the passed in responder object
        handler: AsyncHandler = cast(AsyncHandler, self.dm.apply_handler(request, responder))
        responder = await handler
        self.update_history(responder)

    def update_history(self, responder):
        """Update the history of the responder to account for this state change"""
        # TODO: Append request/response to history, being careful to not make it recursive
