#!/usr/bin/env python3

from src.models import sa, orm, DeclarativeBase, CategoryRelation

class Category(DeclarativeBase):
    """The model for Book data"""
    __tablename__ = "category"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.Unicode(100), unique=True)
    description = sa.Column(sa.Unicode(100))
    kernels = orm.relationship(CategoryRelation,
                               back_populates="category")
