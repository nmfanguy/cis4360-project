import requests
import getpass

if __name__ == "__main__":
    print("welcome to the password manager.")
    url = input("enter the server URL you would like to use: ")

    if not url.startswith("http://"):
        url = "http://" + url

    # check the URL
    try:
        requests.get(f"{url}/api/ping")
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

        
        res = requests.post(f"{url}{endpoint}", data={"username": username, "password": password})
        if res.ok:
            token = res.json()["token"]
            break
        else:
            print("error: could not log you in. please try again.")
    
    # REPL
    while True:
        cmd = input("passwords> ")

        if cmd in ["q", "quit", "exit"]:
            print("see you later!")
            exit(0)
