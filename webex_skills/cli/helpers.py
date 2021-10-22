from webex_skills.supress_warnings import suppress_warnings


def create_nlp(app_path):
    try:
        with suppress_warnings():
            from mindmeld.components.nlp import NaturalLanguageProcessor
    except ImportError:
        raise ImportError('You must install the extras package webex-assistant-sdk[mindmeld] to use NLP commmands')
    nlp = NaturalLanguageProcessor(app_path=app_path)
    return nlp
