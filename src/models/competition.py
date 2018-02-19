from src.models import orm, Base, DeclarativeBase
from src.models.categoty_relation import CategoryRelation
from src.models.kernel import Kernel

class Competition(Base, DeclarativeBase):
    """The model for Book data"""
    __tablename__ = "competition"

    categories = orm.relationship(CategoryRelation,
                                  back_populates="competition")
    kernels = orm.relationship(Kernel,
                               back_populates='competition')
