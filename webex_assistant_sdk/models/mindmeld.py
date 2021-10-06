from pydantic import BaseModel


class MindmeldRequest(BaseModel):
    pass


class MindmeldResponse(BaseModel):
    pass


"""@attr.s(frozen=True, kw_only=True)  # pylint: disable=too-many-instance-attributes
class Request:
    # 
    # The Request is an object passed in through the Dialogue Manager and contains all the
    # information provided by the application client for the dialogue handler to act on. Note: the
    # Request object is read-only since it represents the client state, which should not be mutated.
    #
    # Attributes:
    #     domains (str): Domain of the current query.
    #     intent (str): Intent of the current query.
    #     entities (list of dicts): A list of entities in the current query.
    #     history (list of dicts): List of previous and current responder objects
    #         (de-serialized) up to the current conversation.
    #     text (str): The query text.
    #     frame (): Immutables Map of stored data across multiple dialogue turns.
    #     params (Params): An object that modifies how MindMeld process the current turn.
    #     context (dict): Immutables Map containing front-end client state that is passed to the
    #         application from the client in the request.
    #     confidences (dict): Immutables Map of keys ``domains``, ``intents``, ``entities``
    #         and ``roles`` containing confidence probabilities across all labels for
    #         each classifier.
    #     nbest_transcripts_text (tuple): List of alternate n-best transcripts from an ASR system
    #     nbest_transcripts_entities (tuple): List of lists of extracted entities for each of the
    #         n-best transcripts.
    #     nbest_aligned_entities (tuple): List of lists of aligned entities for each of the n-best
    #         transcripts.
    #
    domain = attr.ib(default=None)
    intent = attr.ib(default=None)
    entities = attr.ib(
        default=attr.Factory(tuple), converter=deserialize_to_list_immutable_maps
    )
    history = attr.ib(
        default=attr.Factory(tuple), converter=deserialize_to_list_immutable_maps
    )
    text = attr.ib(default=None)
    frame = attr.ib(default=immutables.Map(), converter=immutables.Map)
    params = attr.ib(default=FrozenParams())
    context = attr.ib(default=immutables.Map(), converter=immutables.Map)
    confidences = attr.ib(default=immutables.Map(), converter=immutables.Map)
    nbest_transcripts_text = attr.ib(
        default=attr.Factory(tuple), converter=tuple
    )
    nbest_transcripts_entities = attr.ib(
        default=attr.Factory(tuple), converter=deserialize_to_lists_of_list_of_immutable_maps
    )
    nbest_aligned_entities = attr.ib(
        default=attr.Factory(tuple), converter=deserialize_to_lists_of_list_of_immutable_maps
    )
    form = attr.ib(default=attr.Factory(tuple), converter=immutables.Map)

    def __iter__(self):
        for key, value in DEFAULT_REQUEST_SCHEMA.dump(self).items():
            if value:
                yield key, value
"""
