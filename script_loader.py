import os

import numpy as np
import pygame


def load_script(script_path):
    with open(script_path, 'r') as f:
        script = f.read()
    return script

def run_script(script_path):
    exec(load_script(script_path))