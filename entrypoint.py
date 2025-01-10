#!/usr/bin/env python3
import os
import sys
import subprocess

def main():
    # Perform database migrations
    print("Running migrations...")
    subprocess.run(["python", "manage.py", "migrate"], check=True)

    # Start the application with uvicorn
    print("Starting the application with uvicorn...")
    subprocess.run(["uvicorn", "your_project_name.asgi:application", "--host", "0.0.0.0", "--port", "8000"])

if __name__ == "__main__":
    main()