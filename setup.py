from setuptools import setup

setup(
    name="charminGPTelegramBot",
    version="0.1",
    packages=[
        "tbot",
        "tbot.admin",
        "tbot.control",
        "tbot.utils",
    ],
    install_requires=["python-telegram-bot"],
)
