#!/usr/bin/env python3
import ast
import _ast


class NameStep:
    def __init__(self, name: str):
        self.name = name
        self.count = 1

    def __repr__(self):
        return self.name + "_p2d2_" + str(self.count)

    def __eq__(self, other):
        return self.name == other


class P2D2_Node(_ast.stmt):
    """
    Our nodes cannot be visited by `ast` because the ast iteration relies on a ._fields attribute. See ast.iter_fields
    """

    def __init__(self, src, orig):
        if type(src) == str:
            src = NameStep(src)
        self.src = src
        self.orig = orig
        self._fields = tuple(self.__dict__.keys())


class Selection(P2D2_Node):
    """
    WHERE
    """

    def __init__(self, cols, cond, src, orig):
        self.cols = cols
        self.cond = cond
        super().__init__(src, orig)


class Projection(P2D2_Node):
    """
    SELECT
    """

    def __init__(self, cols, src, orig):
        self.cols = cols
        super().__init__(src, orig)


class Update(P2D2_Node):
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


class P2D2_Assign(P2D2_Node):
    """
    SELECT
    """

    def __init__(self, tar: str, inPlace: bool, src, orig):
        self.tar = NameStep(tar)
        self.inPlace = inPlace
        super().__init__(src, orig)


class DBTable(P2D2_Node):
    """
    SELECT
    """

    def __init__(self, conn, src, orig):
        self.conn = conn
        super().__init__(src, orig)


class Action(P2D2_Node):
    """
    SELECT
    """

    def __init__(self, src, orig):
        super().__init__(src, orig)


class Pull(P2D2_Node):
    """
    SELECT
    """

    def __init__(self, name, src, orig):
        """
        We use 'name' instead of 'tar' (compare P2D2_Assign) because 'tar's get updated in IMR
        """

        self.name = name
        super().__init__(src, orig)


class Ignored(P2D2_Node):
    def __init__(self, tar, src, orig):
        super().__init__(src, orig)
