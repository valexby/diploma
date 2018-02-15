#!/usr/bin/env python3

from sqlalchemy.schema import ForeignKey
from src.models import sa, orm, DeclarativeBase

class TechnologyRelation(DeclarativeBase):
    """The model for Book data"""
    __tablename__ = "technology_relation"

    id = sa.Column(sa.Integer, primary_key=True)
    kernel_id = sa.Column(sa.Integer, ForeignKey("kernel.id"))
    technology_id = sa.Column(sa.Integer, ForeignKey("technology.id"))
    technology = orm.relationship("Technology", back_populates="kernels")
    kernel = orm.relationship("Kernel", back_populates="technologies")
