from src.models import orm, Base, TechnologyRelation, DeclarativeBase

class Technology(Base, DeclarativeBase):
    """The model for Book data"""
    __tablename__ = "technology"

    kernels = orm.relationship(TechnologyRelation, back_populates="technology")
