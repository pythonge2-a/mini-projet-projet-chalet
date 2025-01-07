from sim import __sim__ as sm
from meteo import __meteo__ as mt
from database import __database__ as db
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from chalet.manage import main as manage_main

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        args = sys.argv[2:]
    else:
        command = 'runserver'
        args = ['0.0.0.0:8000']
    
    manage_main(command, *args)

if __name__ == "__main__":
    main()