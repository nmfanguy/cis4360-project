# Password Manager Testing

## Running

This project is using a virtualenv to manage the prisma client and other dependencies.
Before doing, run the following:

```bash
> source bin/activate # only works on non-Windows...
> python3 -m pip install -r requirements.txt
> cd backend
> prisma migrate dev
> cd ..
```

### Backend

Start the Flask server first.

```bash
> cd backend
> py app.py
```

### CLI

Then, in a new window:

```bash
> cd cli
> py run.py
# REPL will start
# the backend is listening on localhost:8888
```