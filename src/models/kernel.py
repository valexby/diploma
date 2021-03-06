import enum

from sqlalchemy.schema import ForeignKey
from src.models import sa, orm, Base, DeclarativeBase
from src.models.categoty_relation import CategoryRelation
from src.models.technology_relation import TechnologyRelation
from src.models.data_link_relation import DataLinkRelation

class Lang(enum.Enum):
    R = 'R'
    Python = 'Python'
    markdown = 'markdown'

class Kernel(Base, DeclarativeBase):
    """The model for Book data"""
    __tablename__ = "kernel"

    lang = sa.Column(sa.Enum(Lang))
    notebook = sa.Column(sa.Boolean)
    votes = sa.Column(sa.Integer)
    best_score = sa.Column(sa.FLOAT)
    source_version = sa.Column(sa.Integer)
    competition_id = sa.Column(sa.Integer, ForeignKey("competition.id"))
    author_id = sa.Column(sa.Integer, ForeignKey("users.id"))
    competition = orm.relationship("Competition", back_populates="kernels")
    author = orm.relationship("User", back_populates="kernels")
    categories = orm.relationship(CategoryRelation,
                                  back_populates="kernel")
    technologies = orm.relationship(TechnologyRelation,
                                    back_populates="kernel")
    data_links = orm.relationship(DataLinkRelation,
                                  back_populates="kernel")
