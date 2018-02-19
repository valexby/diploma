from sqlalchemy.dialects.mysql import VARCHAR
from src.models import sa, orm, Base, DataLinkRelation, DeclarativeBase

class DataLink(Base, DeclarativeBase):
    """The model for Book data"""
    __tablename__ = "data_link"

    link = sa.Column(sa.Unicode(100))
    source_type = sa.Column(VARCHAR(100, charset='utf8'), unique=True)
    kernels = orm.relationship(DataLinkRelation, back_populates="data_link")
