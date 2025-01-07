from sim import __sim__ as sm
from meteo import __meteo__ as mt
from database import __database__ as db
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from chalet.manage import main as manage_main

def main():
    manage_main('runserver', '0.0.0.0:8000')

if __name__ == "__main__":
    main()