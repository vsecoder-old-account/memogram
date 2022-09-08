import sqlalchemy as sa
from .db import SqlAlchemyBase


class Mem(SqlAlchemyBase):
    __tablename__ = 'mems'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer,
                   primary_key=True)
    title = sa.Column(sa.String, nullable=True)
    text = sa.Column(sa.String, nullable=True)
    image = sa.Column(sa.String, nullable=True)
    tag = sa.Column(sa.String, nullable=True)
    likes = sa.Column(sa.String, nullable=True)
    author = sa.Column(sa.Integer, nullable=True)
