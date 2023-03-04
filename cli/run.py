import requests
import getpass

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
            print(f"got: {res.text}")
            token = res.json()["token"]
            break
        else:
            err_message = res.text
            print(f"error: could not log you in. {err_message}. please try again.")
    
    # REPL
    while True:
        cmd = input("passwords> ")

        if cmd in ["q", "quit", "exit"]:
            print("see you later!")
            exit(0)
