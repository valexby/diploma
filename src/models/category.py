from sqlalchemy.dialects.mysql import VARCHAR
from src.models import sa, orm, Base, CategoryRelation, DeclarativeBase

class Category(Base, DeclarativeBase):
    """The model for Category data"""
    __tablename__ = "category"

    description = sa.Column(VARCHAR(100, charset='utf8'))
    kernels = orm.relationship(CategoryRelation,
                               back_populates="category")
