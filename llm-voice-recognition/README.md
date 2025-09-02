# llm-llm-voice-recognition

[![PyPI](https://img.shields.io/pypi/v/llm-llm-voice-recognition.svg)](https://pypi.org/project/llm-llm-voice-recognition/)
[![Changelog](https://img.shields.io/github/v/release/uniesecruz/llm-llm-voice-recognition?include_prereleases&label=changelog)](https://github.com/uniesecruz/llm-llm-voice-recognition/releases)
[![Tests](https://github.com/uniesecruz/llm-llm-voice-recognition/actions/workflows/test.yml/badge.svg)](https://github.com/uniesecruz/llm-llm-voice-recognition/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/uniesecruz/llm-llm-voice-recognition/blob/main/LICENSE)

This project provides a blueprint for building a voice-activated assistant powered by a large language model (LLM). It captures spoken input, transcribes it into text, and then leverages a free generative AI to formulate a coherent and contextually relevant response, which is then synthesized back into speech.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-llm-voice-recognition
```
## Usage

Usage instructions go here.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-llm-voice-recognition
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
python -m pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
