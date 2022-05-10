from models.base import Base

import sqlalchemy as sq
from sqlalchemy.orm import relationship


class Users(Base):

    __tablename__ = 'users'

    user_id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer, nullable=False, unique=True)
    sex = sq.Column(sq.Integer)
    age = sq.Column(sq.Integer)
    city = sq.Column(sq.String(50))
    candidate = relationship('Candidates', secondary='user_candidate', back_populates='candidates', cascade='all,delete')