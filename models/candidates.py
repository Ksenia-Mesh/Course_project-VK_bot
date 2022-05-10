from models.base import Base

import sqlalchemy as sq
from sqlalchemy.orm import relationship


class Candidates(Base):

    __tablename__ = 'candidates'

    candidate_id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String(50))
    last_name = sq.Column(sq.String(50))
    link = sq.Column(sq.String, nullable=False, unique=True)
    user = relationship('Users', secondary='user_candidate', back_populates='users', cascade='all,delete')
    photo = relationship('Photo')
