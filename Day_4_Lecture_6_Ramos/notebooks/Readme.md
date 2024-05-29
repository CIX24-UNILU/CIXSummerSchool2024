# Readme

This file contains information about how to set your environment to run the code in the notebooks that accompany the course _"Augmenting Ideation and Sensemaking in the age of LLMs: Concepts, Examples, and Opportunities from an HCI Perspective"_.

## Dependencies

- [Git](https://git-scm.com/downloads) - Important for version control and pulling things from repositories (repos).
- [VSCode](https://code.visualstudio.com/download) - A code editor that is very useful for Python development and working with interactive notebooks that run locally. **Highly recommended**.
- [poetry](https://python-poetry.org/docs/#installation) - A (recommended) tool for managing Python dependencies.

## A note about python versions

At the time of writing this file we use Python 3.11.3. We recommend that you use [pyenv-win](https://github.com/pyenv-win/pyenv-win) or [pyenv](https://github.com/pyenv/pyenv) to both install and manage different versions of Python. We recommend that you uninstall any other version of Python you might have installed in your system and use pyenv to install the version we use (3.11). After you have installed pyenv, you can install the version we use with the following command:

```bash
pyenv install 3.11.3
```

and then select it as the version to use with the following command:

```bash
pyenv global 3.11.3
```

After you make sure you have version 3.11 installed, you now can install the dependencies for the backend to run. **We strongly recommend that you use a python virtual environment for this.** We use [poetry](https://python-poetry.org/docs/#installation) to do this and the files `pyproject.toml` and `poetry.lock` can be used to recreate the environment we use. One simply does this by running `poetry install` in the project's root directory.

## Notebooks

### parsebookmarks

This has code that can help you parse the exported bookmarks from your browser.

### html_utils

This has code that can help you do some basic processing of HTML files.

### using_llms

This file can help you get up and running using LLMs with simple examples.

### using_embeddings

Embeddings are useful to assess the semantic similarity of different parts of documents. This file can help you get up and running using embeddings with simple examples.

### using_agents (optional)

Agents can be a powerful abstraction to help you do more complex tasks with LLMs. This file can help you get up and running using agents with simple examples.

## Data

## Questions?

Reach out to me at [email](mailto:gonzo.ramos@gmail.com).