# Webex Assistant Skills SDK

The Webex Skills SDK is designed to simplify the process of creating a Webex Assistant Skill. It provides some
tools that help to easily set up a template skill, deal with encryption and test the skill locally, among other
things.

This is a simplified version of the documentation, for more information visit the official  
[Webex Assistant Skills SDK website](https://developer.webex.com/docs/api/guides/webex-assistant-skills-guide).

## Installing the SDK

This SDK supports `Python 3.7` and above. If you want to be able to build
[MindMeld Skills](https://developer.webex.com/docs/api/guides/webex-assistant-skills-guide#building-a-mindmeld-skill),
you will need to use `Python 3.7` for compatibility with the [MindMeld library](https://www.mindmeld.com/).

### Using pip

Create a virtual environment with `Python 3.7`:

```python
pyenv install 3.7.5
pyenv virtualenv 3.7.5 webex-skills
pyenv local webex-skills
```

Install using `pip`:

```python
pip install webex-skills
```

In order to build `MindMeld Skills` you need the `mindmeld` extra:

```python
pip install 'webex-skills[mindmeld]'
```

### Install from Source

You can install from source using `Poetry`. Set up python 3.7.5 locally:

```python
pyenv install 3.7.5
pyenv local 3.7.5
```

Now you can run `Poetry`'s `install` command:

```python
poetry install
```

In order to build `MindMeld Skills` you need the `mindmeld` extra:

```python
poetry install --extras "mindmeld"
```


## Building Skills

You can follow the next guides for building your first skills:

- [Simple Skills vs MindMeld Skills](https://developer.webex.com/docs/api/guides/webex-assistant-skills-guide#simple-skills-vs-mindmeld-skills)
- [Building a Simple Skill](https://developer.webex.com/docs/api/guides/webex-assistant-skills-guide#building-a-simple-skill)
- [Building a MindMeld Skill](https://developer.webex.com/docs/api/guides/webex-assistant-skills-guide#building-a-mindmeld-skill)
