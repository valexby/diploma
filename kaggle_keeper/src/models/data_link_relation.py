#!/usr/bin/env python3

from src.models import sa, orm, DeclarativeBase, DataLink, Kernel

class DataLinkRelation(DeclarativeBase):
    """The model for Book data"""
    __tablename__ = "data_link_relation"

    id = sa.Column(sa.Integer, primary_key=True)
    kernel_id = sa.Column(sa.Integer)
    data_link_id = sa.Column(sa.Integer)

    category = orm.relationship(
        data_link_id,
        primaryjoin=orm.remote(DataLink.id) == data_link_id,
    )

    kernel = orm.relationship(
        Kernel,
        primaryjoin=orm.remote(Kernel.id) == kernel_id,
    )
