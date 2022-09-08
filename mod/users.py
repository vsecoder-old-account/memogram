import sqlalchemy as sa
from .db import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer,
                   primary_key=True)
    name = sa.Column(sa.String)
    email = sa.Column(sa.String)
    tags = sa.Column(sa.String)
    token = sa.Column(sa.String)
