from models.base import Base

import sqlalchemy as sq


class Photos(Base):

    __tablename__ = 'photos'

    photo_id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer, nullable=False, unique=True)
    like_count = sq.Column(sq.Integer, nullable=False)
    candidate_id = sq.Column(sq.Integer, sq.ForeignKey('candidates.candidate_id'))