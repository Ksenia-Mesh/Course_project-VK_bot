from models.base import Base

import sqlalchemy as sq


class UserCandidate(Base):

    __tablename__ = 'users_candidates'

    __table_args__ = (sq.PrimaryKeyConstraint('user_id', 'candidate_id'), )

    user_id = sq.Column(sq.Integer, sq.ForeignKey('users.user_id'))
    candidate_id = sq.Column(sq.Integer, sq.ForeignKey('candidates.candidate_id'))

