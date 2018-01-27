#!/usr/bin/env python3

from src.models import sa, orm, DeclarativeBase, Technology, Kernel

class TechnologyRelation(DeclarativeBase):
    """The model for Book data"""
    __tablename__ = "technology_relation"

    id = sa.Column(sa.Integer, primary_key=True)
    kernel_id = sa.Column(sa.Integer)
    technology_id = sa.Column(sa.Integer)

    category = orm.relationship(
        Technology,
        primaryjoin=orm.remote(Technology.id) == technology_id,
    )

    kernel = orm.relationship(
        Kernel,
        primaryjoin=orm.remote(Kernel.id) == kernel_id,
    )
