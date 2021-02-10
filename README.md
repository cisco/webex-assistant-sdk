# Webex Assistant SDK

An SDK for developing Webex Assistant Skills based on the [MindMeld](https://www.mindmeld.com) platform.

## Install the SDK

`pip install webex_assistant_sdk`

## Using the SDK

To use the SDK we just need to import SkillApplication and pass in the RSA private key as well as the secret for verifying the request's header.

Here is an example implementation which is found in the `tests` folder:

```python
from pathlib import Path

from webex_assistant_sdk import SkillApplication
from webex_assistant_sdk.crypto import load_private_key_from_file

secret = 'some secret'
key = load_private_key_from_file(Path(__file__).resolve().parent / 'id_rsa'), password=None)
app = SkillApplication(__name__, secret=secret, private_key=key)

__all__ = ['app']
```

Similar to MindMeld applications, for development convenience, we have included a Flask server for you to test your application.

To run the development server you can use the `run` command: `python -m [app] run`.

We do not recommend using the development server for production purpose. To learn more about productionizing Flask application, please check [Deployment Options](https://flask.palletsprojects.com/en/1.1.x/deploying/).

### The introduce decorator

The SkillApplication adds a `introduce` decorator in addition to MindMeld's build in decorator. This is used to mark the dialogue state to use when a user calls a skill without any command, i.e. "talk to <skill-name>"

#### Example

```python
@app.introduce
def introduction(request, responder):
    pass
```

### Debugging

To debug the server and turn off encryption/decryption, you can set the environment variable `WXA_SKILL_DEBUG` to be `True`.

### Command Line

Installing the webex_assistant_sdk package adds a wxa_sdk command line application. Use the `-h` argument for help.

```bash
$ wxa_sdk -h
usage: wxa_sdk [-h] {new,generate-keys,invoke,check} ...

positional arguments:
  {new,generate-keys,invoke,check}
    new                 create a new skill project
    generate-keys       generate keys for use with a Webex Assistant Skill
    invoke              invoke a skill simulating a request from Webex
                        Assistant
    check               check the health and configuration of a Webex
                        Assistant Skill

optional arguments:
  -h, --help            show this help message and exit
```
