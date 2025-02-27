import sys
import os

def set_path()->None:

    sys.path.append(os.path.abspath(os.path.join("..")))

DATA_DIR = '../data'
SAMPLE_STATE=1