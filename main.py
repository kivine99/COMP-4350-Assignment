import click
import requests

BASE_URL = "http://api.combatcritters.ca:4000"

@click.group(
    help="A CLI tool to interact with the Combat Critters API.\n\n"
         "Provided commands allow you to login, get your pack inventory, "
         "view a pack's set list, and open a pack in your inventory",
    epilog="Type 'python3 main.py <command> --help' to get help on a specific command."
)
def cli():
    pass

if __name__ == "__main__":
    cli()
