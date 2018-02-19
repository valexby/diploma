from sqlalchemy.schema import ForeignKey
from src.models import sa, orm, DeclarativeBase

class DataLinkRelation(DeclarativeBase):
    """The model for Book data"""
    __tablename__ = "data_link_relation"

    id = sa.Column(sa.Integer, primary_key=True)
    kernel_id = sa.Column(sa.Integer, ForeignKey("kernel.id"))
    data_link_id = sa.Column(sa.Integer, ForeignKey("data_link.id"))
    data_link = orm.relationship("DataLink", back_populates="kernels")
    kernel = orm.relationship("Kernel", back_populates="data_links")
