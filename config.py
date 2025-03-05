import sys
import os


PROJ_DIR = os.path.dirname(os.path.abspath(__file__))


def set_path()->None:

    sys.path.append(PROJ_DIR)


DATA_DIR: str = os.path.abspath(os.path.join(PROJ_DIR, 'data'))
SAMPLE_STATE=1