from models.base import Base

import sqlalchemy as sq


users_candidates = sq.Table('users_candidates', Base.metadata,
                            sq.Column('user_id', sq.Integer(), sq.ForeignKey('users.user_id')),
                            sq.Column('candidate_id', sq.Integer(), sq.ForeignKey('candidates.candidate_id'))
                            )

