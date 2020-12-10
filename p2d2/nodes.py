#!/usr/bin/env python3
import ast
import _ast

class P2B2_Node(_ast.stmt):
    def __init__(self, src, orig):
        self.src = src
        self.orig = orig

class Selection(P2B2_Node):
    """
    WHERE
    """
    def __init__(self, cols, cond, src, orig):
        super().__init__(src, orig)
        self.cols = cols
        self.cond = cond
        self.src = src
        self.orig = orig


class Projection(P2B2_Node):
    """
    SELECT
    """
    def __init__(self, cols, src, orig ):
        super().__init__(src, orig)


class Update(P2B2_Node):
    """
    SELECT
    """
    def __init__(self, sel, proj, op, src, orig):
        super().__init__(src, orig)

class Join:
    """
    SELECT
    """
    def __init__(self, src):
        super().__init__(src, orig)

        pass

class P2B2_Assign(P2B2_Node):
    """
    SELECT
    """
    def __init__(self, tar, inPlace, src, orig):
        super().__init__(src, orig)
        self.tar=tar
        self.inPlace=inPlace

class DBTable(P2B2_Node):
    """
    SELECT
    """
    def __init__(self, conn, src, orig):
        super().__init__(src, orig)
        self.conn = conn


class Sink(P2B2_Node):
    """
    SELECT
    """
    def __init__(self, src, orig):
        super().__init__(src, orig)
        

class Pull(P2B2_Node):
    """
    SELECT
    """
    def __init__(self, tar, src, orig):
        super().__init__(src, orig)

class Ignored(P2B2_Node):

    def __init__(self, tar, src, orig):
        super().__init__(src, orig)

