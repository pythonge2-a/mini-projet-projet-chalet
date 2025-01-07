import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from chalet.manage import main as manage_main

def main():
    manage_main('runserver', '0.0.0.0:8000')

if __name__ == "__main__":
    main()