#!/usr/bin/python3
import os
import sys
import subprocess

def main():
    # Perform database migrations
    print("Running migrations...")
    subprocess.run(["python", "manage.py", "makemigrations"], check=True)
    subprocess.run(["python", "manage.py", "migrate"], check=True)

    # Start the application with uvicorn python manage.py makemigrations agency
    # python manage.py migrate
    print("Starting the application...")
    subprocess.run(["python", "manage.py", "runserver", "0.0.0.0:8000"])

if __name__ == "__main__":
    main()
