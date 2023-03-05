import requests
import getpass
import pyperclip

class Context:
    def __init__(self, base_url, token, password):
        self.base_url = base_url
        self.token = token
        self.password = password

def get_login_by_name(ctx: Context):
    name = input("service name: ")

    all_res = cmd_get_all(ctx, quiet=True)
    if all_res == None:
        return

    matching_services = list(filter(lambda l: l["service"] == name, all_res))

    if len(matching_services) != 1:
        print(f"error: no service with name {name}")
        return

    matching_service = matching_services[0]
    return matching_service

def cmd_get_all(ctx: Context, quiet = False):
    res = requests.get(f"{ctx.base_url}/api/logins", headers={"Authorization": f"Bearer {ctx.token}"})

    if not res.ok:
        err_message = res.json()["error"]
        if not quiet:
            print(f"error: {err_message}")
        return

    logins = res.json()["logins"]
    logins.sort(key=lambda l: l["service"])
    
    if not quiet:
        print(f"your logins: {logins}")
    return logins

def cmd_get_one(ctx: Context):
    matching_service = get_login_by_name(ctx)

    if matching_service == None:
        return

    res = requests.post(f"{ctx.base_url}/api/logins/{matching_service['id']}", headers={"Authorization": f"Bearer {ctx.token}"}, json={"accountPassword": ctx.password})

    if not res.ok:
        print(f"raw: {res.text}")
        err_message = res.json()["error"]
        print(f"error: {err_message}")
        return

    login = res.json()["login"]

    pyperclip.copy(login["username"])

    input("copied username to the clipboard, press any key to continue...")

    pyperclip.copy(login["password"])

    input("copied password to the clipboard, press any key to continue...")

    pyperclip.copy("") # clear it out

    print("done!")

def cmd_delete_login(ctx: Context):
    matching_service = get_login_by_name(ctx)
    if matching_service == None:
        return

    res = requests.delete(f"{ctx.base_url}/api/logins/{matching_service['id']}", headers={"Authorization": f"Bearer {ctx.token}"}, json={"accountPassword": ctx.password})

    if not res.ok:
        print(f"raw: {res.text}")
        err_message = res.json()["error"]
        print(f"error: {err_message}")
        return

    print("done!")

def cmd_create_login(ctx: Context):
    service = input("service name: ")
    username = input("username: ")
    password = getpass.getpass("password: ")

    payload = {"service": service, "username": username, "password": password, "accountPassword": ctx.password}

    res = requests.post(f"{ctx.base_url}/api/logins", headers={"Authorization": f"Bearer {ctx.token}"}, json=payload)

    if not res.ok:
        err_message = res.json()["error"]
        print(f"error: {err_message}")
        return

    print(f"successfully created login for {service}!")

if __name__ == "__main__":
    print("welcome to the password manager.")
    url = input("enter the server URL you would like to use: ")

    if not url.startswith("http://"):
        url = "http://" + url

    # check the URL
    try:
        res = requests.get(f"{url}/api/ping")
        if res.text != "pong":
            raise Exception("invalid server")
    except:
        print("error: could not connect to server. please try again.")
        exit(1)

    # login
    choice = ""
    token = ""
    password = ""
    while True:
        while choice not in ["1", "2"]:
            choice = input("would you like to (1) register or (2) login? ")

        username = input("username: ")
        password = getpass.getpass("password: ")

        # register
        if choice == "1":
            endpoint = "/api/register"
        elif choice == "2":
            endpoint = "/api/login"
        choice = ""
        
        res = requests.post(f"{url}{endpoint}", json={"username": username, "password": password})
        if res.ok:
            token = res.json()["token"]
            break
        else:
            err_message = res.text
            print(f"error: could not log you in. {err_message}. please try again.")

    ctx = Context(url, token, password)
    
    # REPL
    while True:
        cmd = input("passwords> ")

        if cmd in ["q", "quit", "exit"]:
            print("see you later!")
            exit(0)
        elif cmd in ["help", "h"]:
            print("commands: get-all, create, copy, delete")
        elif cmd == "get-all":
            cmd_get_all(ctx)
        elif cmd == "create":
            cmd_create_login(ctx)
        elif cmd == "copy":
            cmd_get_one(ctx)
        elif cmd == "delete":
            cmd_delete_login(ctx)
        else:
            print("unknown command!")
