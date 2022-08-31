# Simple Telegram Bot

In this repo I am experimenting with some simple telegram bots.

First request an API token for a new bot from the [@BotFather](t.me/BotFather), and then
either store it plaintext in the `.token` file (don't forget `chmod 400 .token` to make
it read-only), or set the `TOKEN` environment variable.

```bash
# token from env
TOKEN="..." python -m tbot

# use `.token` file
python -m tbot
```

## Setup

```bash
# conda deactivate && conda env remove -n telegram-bot

conda create -n telegram-bot "python>=3.9" pip setuptools numpy \
  && conda activate telegram-bot \
  && pip install python-telegram-bot

pip install -e .
```
