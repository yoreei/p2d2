from .ssa import ssa
from .anf import anf
from .desugar import desugar


def preprocess(code: str):
    return anf(ssa(desugar(code)))
