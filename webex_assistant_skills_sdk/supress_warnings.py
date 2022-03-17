import warnings


class suppress_warnings:  # pylint:disable=invalid-name
    def __init__(self):
        self._showwarning = None

    def showwarning(self, *args, **kwargs):
        pass

    def __enter__(self):
        self._showwarning = warnings.showwarning
        warnings.showwarning = self.showwarning

    def __exit__(self, exc_type, exc_val, exc_tb):
        warnings.showwarning = self._showwarning
