#!/usr/bin/env python3

from sqlalchemy.dialects.mysql import VARCHAR
from src.models import sa, orm, DeclarativeBase, DataLinkRelation

class DataLink(DeclarativeBase):
    """The model for Book data"""
    __tablename__ = "data_link"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(VARCHAR(100, charset='utf8'), unique=True)
    link = sa.Column(sa.Unicode(100))
    source_type = sa.Column(VARCHAR(100, charset='utf8'), unique=True)
    kernels = orm.relationship(DataLinkRelation, back_populates="data_link")
