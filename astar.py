# astar.py

import ctypes
import os
import sys

import numpy as np


class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int), ("y", ctypes.c_int)]


class AStar:
    # Load the shared library once and reuse it
    if sys.platform.startswith('win'):
        lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib', 'astarc.dll'))
    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib', 'libastarc.so'))
    else:
        raise NotImplementedError("Unsupported operating system")
    
    lib = ctypes.CDLL(lib_path)

    # Define return types and argument types for functions
    lib.AStar_new.argtypes = [ctypes.POINTER(ctypes.c_long), ctypes.c_int, ctypes.c_int]
    lib.AStar_new.restype = ctypes.c_void_p

    lib.AStar_find_path.argtypes = [ctypes.c_void_p, Point, Point, Point, ctypes.POINTER(ctypes.c_int)]
    lib.AStar_find_path.restype = ctypes.POINTER(Point)

    lib.AStar_delete.argtypes = [ctypes.c_void_p]
    lib.AStar_delete_path.argtypes = [ctypes.POINTER(Point)]

    def __init__(self, grid):
        self.grid = grid if isinstance(grid, np.ndarray) else np.array(grid, dtype=np.int32)

        # Create AStar instance
        rows, cols = self.grid.shape
        grid_1d = self.grid.flatten()
        self.grid_data_instance = (ctypes.c_long * len(grid_1d))(*grid_1d)
        self.astar = self.lib.AStar_new(self.grid_data_instance, rows, cols)

    def find_path(self, start, end, size=(1, 1)):
        # Find path
        path_length = ctypes.c_int()
        path_ptr = self.lib.AStar_find_path(self.astar, Point(*start), Point(*end), Point(*size), ctypes.byref(path_length))
        path = [(path_ptr[i].x, path_ptr[i].y) for i in range(path_length.value)]
        self.lib.AStar_delete_path(path_ptr)
        return path