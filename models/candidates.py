from models.base import Base

import sqlalchemy as sq
from sqlalchemy.orm import relationship


class Candidates(Base):

    __tablename__ = 'candidates'

    candidate_id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String(50))
    last_name = sq.Column(sq.String(50))
    vk_id = sq.Column(sq.String, nullable=False, unique=True)
    users = relationship('Users', secondary='users_candidates', back_populates='candidates', cascade='all,delete')


