import subprocess
import sys

def install_requirements():
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
    for requirement in requirements:
        subprocess.check_call([sys.executable, "-m", "pip", "install", requirement])

if __name__ == '__main__':
    install_requirements()
