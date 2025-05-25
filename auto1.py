import shutil
import subprocess
import sys

# List of tools to check with their minimum versions
tools = {
    "git": {"cmd": "git --version", "min_version": "2.0"},
    "python3": {"cmd": "python3 --version", "min_version": "3.11"},
    "uv": {"cmd": "uv --version", "min_version": "0.7"},
    "code": {"cmd": "code --version", "min_version": "1.99"}  # VS Code CLI
}

# Python packages to check
python_packages = ["numpy", "pandas", "streamlit"]

# VS Code Extensions to check (using CLI)
vscode_extensions = [
    "ms-python.python",
    "ms-toolsai.jupyter",
    "charliermarsh.ruff",
    "ms-vscode.vscode-pylance"
]


def check_version(command, required_version):
    try:
        output = subprocess.check_output(command.split(), stderr=subprocess.STDOUT).decode()
        version = ''.join([s for s in output if s.isdigit() or s == '.']).split()[0]
        return float(version) >= float(required_version)
    except Exception as e:
        return False


def check_tools():
    print("🔍 Checking system tools:")
    for name, info in tools.items():
        if shutil.which(name) is None:
            print(f"❌ {name} is not installed.")
        else:
            if check_version(info["cmd"], info["min_version"]):
                print(f"✅ {name} is installed and version is OK.")
            else:
                print(f"⚠️ {name} is installed but version is below {info['min_version']}")


def check_python_packages():
    print("\n📦 Checking Python packages:")
    for pkg in python_packages:
        try:
            __import__(pkg)
            print(f"✅ {pkg} is installed.")
        except ImportError:
            print(f"❌ {pkg} is NOT installed.")


def check_vscode_extensions():
    print("\n🧩 Checking VS Code extensions (requires `code` CLI):")
    try:
        output = subprocess.check_output(["code", "--list-extensions"]).decode().splitlines()
        for ext in vscode_extensions:
            if ext in output:
                print(f"✅ {ext} is installed.")
            else:
                print(f"❌ {ext} is NOT installed.")
    except FileNotFoundError:
        print("⚠️ VS Code CLI not found. Run `Shell Command: Install 'code' command in PATH` from VS Code.")

        
if __name__ == "__main__":
    check_tools()
    check_python_packages()
    check_vscode_extensions()
