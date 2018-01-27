#!/usr/bin/env python3

import enum

from src.models import sa, DeclarativeBase

class Lang(enum.Enum):
    r = 'R'
    python = 'Python'

class Kernel(DeclarativeBase):
    """The model for Book data"""
    __tablename__ = "kernel"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.Unicode(20))
    lang = sa.Column(sa.Enum(Lang))
    notebook = sa.Column(sa.Boolean)
    votes = sa.Column(sa.Integer)
