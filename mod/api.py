from mod.db import create_session
from mod.mems import Mem
from mod.users import User
from mod.utils import generate_key
from sqlalchemy_pagination import paginate

import sqlalchemy


class API:

    def check_token(id, token):
        print(API.get_token(id))
        if token == API.get_token(id):
            return True
        return False

    def get_token(id):
        try:
            session = create_session()

            user = session.query(User).\
                        filter(User.id == id).\
                        one()

            return user.token
        except sqlalchemy.exc.NoResultFound:
            return None

    def create_user(name, email):
        token = generate_key()
        session = create_session()

        user = User(
            name=name,
            email=email,
            tags='[]',
            token=token
        )
        session.add(user)
        session.commit()
        return token

    def create_mem(title, text, image, token, tag, id):
        if not API.check_token(id, token):
            return False

        session = create_session()

        mem = Mem(
            title=title,
            text=text,
            image=image,
            author=id,
            likes='[]',
            tag=tag
        )
        session.add(mem)
        session.commit()
        return True

    def get_mem(id):
        try:
            session = create_session()

            mem = session.query(Mem).\
                        filter(Mem.id == id).\
                        one()

            result = Mem(
                id=mem.id,
                title=mem.title,
                text=mem.text,
                image=mem.image,
                tag=mem.tag,
                likes=mem.likes
            )
            return result
        except sqlalchemy.exc.NoResultFound:
            return None

    def get_user(id):
        try:
            session = create_session()

            user = session.query(User).\
                        filter(User.id == id).\
                        one()

            result = User(
                id=user.id,
                name=user.name,
                tags=user.tags
            )
            return result
        except sqlalchemy.exc.NoResultFound:
            return None

    def get_hot_mems(a, b):
        session = create_session()
        mems = paginate(session.query(Mem), int(a), int(b))

        return mems


    def get_rec_mems(id, a, b):
        session = create_session()
        user = API.get_user(id)

        mems = paginate(session.query(Mem).filter(user.tags == Mem.tag), int(a), int(b))
        return mems
