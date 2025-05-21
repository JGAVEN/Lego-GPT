"""Minimal numpy stub for offline tests."""

class ndarray(list):
    pass

def zeros(shape, dtype=None):
    if isinstance(shape, int):
        shape = (shape,)
    if len(shape) == 1:
        return [0] * shape[0]
    if len(shape) == 2:
        return [[0] * shape[1] for _ in range(shape[0])]
    if len(shape) == 3:
        return [[[0] * shape[2] for _ in range(shape[1])] for _ in range(shape[0])]
    raise NotImplementedError

def array(data, dtype=None):
    return data
