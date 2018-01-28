#!/usr/bin/env python3

from src.models import sa, orm, DeclarativeBase, DataLinkRelation

class DataLink(DeclarativeBase):
    """The model for Book data"""
    __tablename__ = "data_link"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.Unicode(20))
    link = sa.Column(sa.Unicode(20))
    kernels = orm.relationship(DataLinkRelation, back_populates="data_link")
