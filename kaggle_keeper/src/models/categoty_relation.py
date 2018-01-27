#!/usr/bin/env python3

from src.models import sa, orm, DeclarativeBase, Category, Kernel

class CategoryRelation(DeclarativeBase):
    """The model for Book data"""
    __tablename__ = "category_relation"

    id = sa.Column(sa.Integer, primary_key=True)
    kernel_id = sa.Column(sa.Integer)
    category_id = sa.Column(sa.Integer)

    category = orm.relationship(
        Category,
        primaryjoin=orm.remote(Category.id) == category_id,
    )

    kernel = orm.relationship(
        Kernel,
        primaryjoin=orm.remote(Kernel.id) == kernel_id,
    )
