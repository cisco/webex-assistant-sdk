from webex_skills.supress_warnings import suppress_warnings


def create_nlp(app_path):
    try:
        with suppress_warnings():
            from mindmeld.components.nlp import NaturalLanguageProcessor  # pylint:disable=import-outside-toplevel
    except ImportError as import_exc:
        error_text = 'You must install the extras package webex-assistant-sdk[mindmeld] to use NLP commmands'
        raise ImportError(error_text) from import_exc
    nlp = NaturalLanguageProcessor(app_path=app_path)
    return nlp
