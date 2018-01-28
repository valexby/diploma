#!/usr/bin/env python3

import enum

from sqlalchemy.ext.declarative import declared_attr
from src.models import sa, orm, DeclarativeBase
from src.models.categoty_relation import CategoryRelation
from src.models.technology_relation import TechnologyRelation
from src.models.data_link_relation import DataLinkRelation

class Lang(enum.Enum):
    r = 'R'
    python = 'Python'

class Kernel(DeclarativeBase):
    """The model for Book data"""
    __tablename__ = "kernel"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.Unicode(100))
    lang = sa.Column(sa.Enum(Lang))
    notebook = sa.Column(sa.Boolean)
    votes = sa.Column(sa.Integer)
    categories = orm.relationship(CategoryRelation,
                                  back_populates="kernel")
    technologies = orm.relationship(TechnologyRelation,
                                   back_populates="kernel")
    data_links = orm.relationship(DataLinkRelation,
                                  back_populates="kernel")
