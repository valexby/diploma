#!/usr/bin/env python3

from sqlalchemy.dialects.mysql import VARCHAR
from src.models import sa, orm, DeclarativeBase
from src.models.categoty_relation import CategoryRelation
from src.models.kernel import Kernel

class Competition(DeclarativeBase):
    """The model for Book data"""
    __tablename__ = "competition"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(VARCHAR(100, charset='utf8'))
    categories = orm.relationship(CategoryRelation,
                                  back_populates="competition")
    kernels = orm.relationship(Kernel,
                               back_populates='competition')
