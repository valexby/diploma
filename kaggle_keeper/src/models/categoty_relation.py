#!/usr/bin/env python3

from sqlalchemy.schema import ForeignKey
from src.models import sa, orm, DeclarativeBase

class CategoryRelation(DeclarativeBase):
    """The model for Book data"""
    __tablename__ = "category_relation"

    id = sa.Column(sa.Integer, primary_key=True)
    kernel_id = sa.Column(sa.Integer, ForeignKey("kernel.id"))
    category_id = sa.Column(sa.Integer, ForeignKey("category.id"))
    category = orm.relationship("Category", back_populates="kernels")
    kernel = orm.relationship("Kernel", back_populates="categories")
