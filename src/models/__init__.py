#!/usr/bin/env python3
"""SQLAlchemy models for the application

In a smaller application you could have all models in this file, but we 
assumed this will grow and have there split things up, in which case you 
should import you sub model at the bottom of this module.
"""

import sqlalchemy as sa
from sqlalchemy import orm
import sqlalchemy.sql as sasql
from sqlalchemy.ext import declarative
from sqlalchemy.ext.hybrid import hybrid_property

maker = orm.sessionmaker(autoflush=True, autocommit=False)
db_session = orm.scoped_session(maker)

class ReprBase(object):
    """Extend the base class

    Provides a nicer representation when a class instance is printed.
    
    Found on the SA wiki, not included with TG
        
    """
    def __repr__(self):
        return "%s(%s)" % (
                 (self.__class__.__name__),
                 ', '.join(["%s=%r" % (key, getattr(self, key))
                            for key in sorted(self.__dict__.keys())
                            if not key.startswith('_')]))

DeclarativeBase = declarative.declarative_base(cls=ReprBase)
metadata = DeclarativeBase.metadata

def init_model(engine):
    """Call me before using any of the tables or classes in the model."""
    db_session.configure(bind=engine)

# you could have your models defined within this module, for larger applications
# it is probably nicer to work with to have them in separate modules and
# import them as shown below.
#
# remember to define __ALL__ in each module

# Import your model modules her.
from src.models.base import *
from src.models.competition import *
from src.models.kernel import *
from src.models.category import *
from src.models.categoty_relation import *
from src.models.technology import *
from src.models.technology_relation import *
from src.models.data_link import *
from src.models.data_link_relation import *
from src.models.user import *
