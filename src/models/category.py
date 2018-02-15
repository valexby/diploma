#!/usr/bin/env python3

from sqlalchemy.dialects.mysql import VARCHAR
from src.models import sa, orm, DeclarativeBase, CategoryRelation

class Category(DeclarativeBase):
    """The model for Book data"""
    __tablename__ = "category"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(VARCHAR(100, charset='utf8'), unique=True)
    description = sa.Column(VARCHAR(100, charset='utf8'))
    kernels = orm.relationship(CategoryRelation,
                               back_populates="category")
