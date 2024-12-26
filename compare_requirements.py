import subprocess
from pathlib import Path

def get_installed_packages():
    # Get list of installed packages using pip
    result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)
    return set(result.stdout.splitlines())

def get_requirements():
    # Read existing requirements.txt
    try:
        with open('requirements.txt', 'r') as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set()

def main():
    installed = get_installed_packages()
    required = get_requirements()
    
    # Find new packages
    new_packages = installed - required
    
    print("New packages to add to requirements.txt:")
    for package in sorted(new_packages):
        print(package)
    
    # Option to update requirements.txt
    if new_packages:
        choice = input("\nWould you like to add these packages to requirements.txt? (y/n): ")
        if choice.lower() == 'y':
            with open('requirements.txt', 'a') as f:
                for package in sorted(new_packages):
                    f.write(f"{package}\n")
            print("requirements.txt has been updated!")

if __name__ == "__main__":
    main() 