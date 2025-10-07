# UnhingedMF

A feral, witty terminal chatbot that talks like your chaotic best friend. Powered by Google Gemini, built for maximum vibes.

## Features

- **Multiple personalities**: unhinged, feral, sweet, or sassy
- **Persistent memory**: remembers your conversations
- **Beautiful terminal UI**: powered by Rich
- **Customizable**: tweak model, temperature, and persona
- **Fast and lightweight**: pure Python, minimal dependencies

## Quick Start

```bash
# Get your Gemini API key from https://makersuite.google.com/app/apikey

# Set it in your environment
export GEMINI_API_KEY="your-key-here"

# Install
pip install -e .

# Run
unhingedmf
```

## Usage

```bash
# Basic usage
unhingedmf

# Choose personality
unhingedmf --persona feral

# Use different model
unhingedmf --model gemini-1.5-pro

# Adjust temperature (creativity)
unhingedmf --temp 1.5

# Clear history
unhingedmf --reset
```

## In-Chat Commands

- `/quit` - exit the chat
- `/reset` - clear conversation history
- `/persona <name>` - switch personality (unhinged, feral, sweet, sassy)
- `/model <name>` - change AI model

## Project Structure

```
unhingedmf/
├── __init__.py       # package initialization
├── cli.py            # main CLI interface
├── chat.py           # chat session management
├── personas.py       # personality system
├── storage.py        # history and config storage
├── pyproject.toml    # project metadata
└── README.md         # this file
```

## Configuration

Config and history are stored in `~/.unhingedmf/`:
- `config.json` - model, persona, temperature settings
- `history.json` - conversation history

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Format code
black unhingedmf/

# Lint
ruff check unhingedmf/
```

## Requirements

- Python 3.10+
- Google Gemini API key
- Terminal with color support

## License

MIT

## Author

Rehana Rahman
