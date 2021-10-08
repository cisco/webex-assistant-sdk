# Webex Assistant SDK

The Webex Assistant SDK is designed to simplify the process of creating a Webex Assistant Skill.
It provides some tools that help to easily set up a template skill, deal with encryption and 
test the skill locally, among other things.

In this document we'll go through some examples of how to use this SDK to create different types
of skills, and we'll also show how to use the different tools available.

## Overview

In this documentation we are going to look at the following topics:

- [Requirements](#requirements)
  - [Installing the SDK](#installing-the-sdk)
- [Simple Skills vs MindMeld Skills](#simple-skills-vs-mindmeld-skills)
  - [Simple Skills](#simple-skills)
  - [MindMeld Skills](#mindmeld-skills)
- [Building a Simple Skill](#building-a-simple-skill)
- [Building a MindMeld Skill](#building-a-mindmeld-skill)
- [Encryption](#encryption)
    - [Generating Secrets](#generating-secrets)
    - [Generating Keys](#generating-keys)
  
## Requirements

In order to follow the examples in this guide, we'll need to install the SDK and its dependencies. Right
now the SDK works with Python 3.7 and above. Note that if you want to build a `MindMeld Skill` as shown
later in the guide you will have to use either Python 3.7 or 3.8, since those are the only supported versions
for the `MindMeld Library`.

### Installing the SDK

We'll start by creating a `pyenv` environment:

```bash
pyenv install 3.7.5
pyenv local 3.7.5
```

We can now install the SDK using `pip`:

```bash
pip install webex-assistant-sdk
```

We should be all set, we'll use the SDK later in this guide.

## Simple Skills vs MindMeld Skills

In a nutshell, a skill is a web service that takes a request containing some text and some context,
analyzes that information and responds accordingly. The level of analysis done on that information
will depend greatly on the tasks the skills has to accomplish. Some skills will simply need to look
for keywords in the text, while others will perform complex NLP in order to understand what the user
is requesting.

This SDK has tooling for creating 2 types of skills: `Simple Skills` and `MindMed Skills`. These should 
serve as templates for basic and complex skills. Let's now take a look at these templates in detail.

### Simple Skills

`Simple Skills` do not perform any type of ML or NLP analysis on the requests. These skills are a good
starting point for developers to start tinkering with, and they are usually good enough for performing
trivial non-complicated tasks. Most developers would start with a `Simple Skill` and then migrate to a
`MindMed Skill` if needed.

Most of the time all you need is to recognize a few keywords in the text. Imagine a skill which only task
is to turn on and off the lights in the office. Some typical queries would be:

- "Turn on the lights" 
- "Turn off the lights" 
- "Turn on the lights please" 
- "Turn the lights off" 

In this particular case, it will probably be good enough to just look for the words `on` and `off` in the
text received. If `on` is present, the skill turns on the lights and responds accordingly and vice versa.

As you can imagine, we don't really need any complex NLP for this skill. A simple regex would be more
than enough. `Simple Skills` do just that: they provide a template where you can specify the regexes you
care about and have them map to specific handlers (`turn_on_lights` and `turn_off_lights` in our example).

We'll build a simple skill in [this section](#building-a-simple-skill)  

### MindMeld Skills

`MindMeld Skills` perform NLP analysis on the requests. These skills are a good template for cases where the
queries will have a lot of variation and contain a lot of information. 

Let's take the case of a skill for ordering food. Queries for a skill like this might look like the following:

- "Order a pepperoni pizza from Super Pizzas"
- "Order a pad thai from Thailand Cafe"
- "I want a hamburger with fries and soda from Hyper Burgers"

As we can see, using regexes for these cases can get out of hand really fast. We would need to be able to
recognize every single dish from every single restaurant, which might account for hundreds or thousands of regexes.
As we add more dishes and restaurants, updating the codebase becomes a real problem.

For cases like this, we leverage the open source [MindMeld Library](https://www.mindmeld.com/). This library makes
it really easy to perform NLP on any text query and identify entities like `dishes`, `restaurants` and `quantities`.
With that, performing the required actions becomes a much easier job.

We'll build a MindMeld skill in [this section](#building-a-mindmeld-skill)

## Building a Simple Skill

Let's now use the SDK to build a `Simple Skill`. As in the example above, we'll build a skill to turn lights on and
off according to what the user is asking. We are going to call this skill `Switch`.

In the `pyenv` environment we created before, run the following command:

```bash
wxa_sdk project init switch
```

This will create a template for a simple skill. You should see the following file structure:
![File Structure](images/switch_directory.png)

As you can see, the `project init` command creates a template of a skill. The arguments you can pass to this 
command are the following:

- 

### Create the Skill Template



## Building a MindMeld Skill

## Encryption
### Generating Secrets
### Generating Keys
