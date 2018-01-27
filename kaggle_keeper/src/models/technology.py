#!/usr/bin/env python3

from src.models import sa, DeclarativeBase

class Technology(DeclarativeBase):
    """The model for Book data"""
    __tablename__ = "technology"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.Unicode(20))
