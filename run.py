import sys, os

commands = [
    ".\\venv\\Scripts\\pip install --upgrade pip",
    ".\\venv\\Scripts\\pip install -r requirements.txt",
    ".\\venv\\Scripts\\python.exe app.py"
]

if __name__ == "__main__":
    for command in commands:
        print(f"Running command: {command}")
        os.system(command)