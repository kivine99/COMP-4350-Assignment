import click
import requests
import os
import json

BASE_URL = "http://api.combatcritters.ca:4000"

@click.group(
    help="A CLI tool to interact with the Combat Critters API.\n\n"
         "Provided commands allow you to login, get your pack inventory, "
         "view a pack's set list, and open a pack in your inventory",
    epilog="Type 'python3 main.py <command> --help' to get help on a specific command."
)
def cli():
    pass

"""Command to log into Combat Critters"""
@cli.command(help="Logs in and saves the session cookie and user ID.")
@click.option("--username", prompt="Username", help="Your username for the Combat Critters")
@click.option("--password", prompt="Password", hide_input=True, confirmation_prompt=False, help="Your password for Combat Critters")
def login(username, password):
    login_url = f"{BASE_URL}/users/auth/login"
    login_payload = {"username": username, "password": password}
    
    try:
        response = requests.post(login_url, json=login_payload)
        
        if response.status_code == 200:
            session_cookie = response.cookies.get("JSESSIONID")
            user_id = response.json().get("id")
            
            # Save session_cookie and user_id into their own files
            if session_cookie and user_id:
                with open("session_cookie.txt", "w") as cookie_file:
                    cookie_file.write(session_cookie)
                with open("user_id.txt", "w") as user_id_file:
                    user_id_file.write(str(user_id))
                
                click.echo("Login successful! Session cookie and user ID saved.")
            else:
                click.echo("Login failed.")
        else:
            click.echo(f"{response.status_code}: Login failed. {response.text}")
    
    except requests.RequestException as error:
        click.echo(f"Error: {error}")



"""Command to fetch packs in the user's inventory"""
@cli.command(help="Fetches the packs in your inventory. Must be logged in.")
def get_packs():
    # Check if the user's logged in (sort of)
    if not os.path.exists("session_cookie.txt") or not os.path.exists("user_id.txt"):
        click.echo("You must log in first.")
        return
    
    # Grab the session cookie
    with open("session_cookie.txt", "r") as cookie_file:
        session_cookie = cookie_file.read().strip()
    #Grab the user's ID
    with open("user_id.txt", "r") as user_id_file:
        user_id = user_id_file.read().strip()
    
    packs_url = f"{BASE_URL}/users/{user_id}/packs"
    
    headers = {
        "Cookie": f"JSESSIONID={session_cookie}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(packs_url, headers=headers)
        
        if response.status_code == 200:
            packs = response.json()
            if len(packs) > 0:
                click.echo("User's Packs:")
                click.echo(json.dumps(packs, indent=4)) 
            else:
                click.echo("You have no packs.")
        else:
            click.echo(f"{response.status_code}: Failed to fetch packs. {response.text}")
    
    except requests.RequestException as error:
        click.echo(f"Error: {error}")


if __name__ == "__main__":
    cli()
