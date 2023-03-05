import os, argparse

import openai

from rich.text import Text
from rich.console import Console

console = Console()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", dest="file", type=str, nargs="?", default=None, help="File to read [optional]")
    parser.add_argument("--temp", "-t", dest="temperature", type=float, nargs="?", default=None, help="Model temperature [optional]")
    parser.add_argument("--maxt", "-mt", dest="max_tokens", type=int, nargs="?", default=None, help="Max tokens to output [optional]")
    parser.add_argument("--apikey", "-k", dest="api_key", type=int, nargs="?", default=None, help="API key. If not given, it will be read from the environment variable OPENAI_API_KEY [optional]")
    return parser.parse_args()


history = [
    # {"role": "system", "content": "You are a helpful assistant."},
]

extra_kw = {}
args = parse_args()
if args.file:
    with open(args.file, "r") as f:
        history.append({"role": "user", "content": "I will ask question about this file" + f.read()})
if args.temperature:
    extra_kw["temperature"] = args.temperature
if args.max_tokens:
    extra_kw["max_tokens"] = args.max_tokens


# set api key
if args.api_key:
    openai.api_key = args.api_key
else:
    openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    console.print("[bold red]Please set OPENAI_API_KEY environment variable[/]")
    exit(1)

while q := console.input("[bold red]> [/]"):
    history.append({"role": "user", "content": q})

    r = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history,
        **extra_kw,
    )
    out = r["choices"][0]["message"]["content"]
    formated_out = Text(out, justify="right")
    history.append({"role": "assistant", "content": out})
    console.print(f"\n[bold green]{out}[/]\n")
