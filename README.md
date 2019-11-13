# Webex Assistant SDK

An SDK for developing Webex Assistant extensions based on the [MindMeld](www.mindmeld.com) platform.

## Install the SDK

`pip install webex_assistant_sdk`

## Using the SDK

To use the SDK we just need to import AgentApplication and pass in the RSA private key as well as the secret for verifying the request's header.

Here is an example implementation which is found in the `tests` folder:

```
import os

from webex_assistant_sdk import AgentApplication
from webex_assistant_sdk.crypto import load_private_key_from_dir

secret = 'some secret'
key = load_private_key_from_dir(os.path.realpath(os.path.dirname(__file__)), password=None)
app = AgentApplication(__name__, secret=secret, private_key=key)

__all__ = ['app']
```

Similar to MindMeld application, for development convenience, we have included a Flask server for you to test your application.

To run the development server you can use the `run` command: `python -m [app] run`.

We do not recommend using the development server for production purpose. To learn more about productionizing Flask application, please check [Deployment Options](https://flask.palletsprojects.com/en/1.1.x/deploying/).