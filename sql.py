import os
import threading
from sqlalchemy import create_engine, delete
from sqlalchemy import Column, TEXT, Numeric, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import uuid

import pymysql
pymysql.install_as_MySQLdb()

id = uuid.uuid1()


BASE = declarative_base()

class Broadcast(BASE):
    __tablename__ = "broadcast"
    id = Column(Numeric, primary_key=True)
    user_name = Column(TEXT)

    def __init__(self, id, user_name):
        self.id = id
        self.user_name = user_name

class AddProduct(BASE):
    __tablename__ = "products"

    unique_id = Column(String(50), primary_key=True)
    user_id = Column(Numeric)
    product_name = Column(TEXT)

    def __init__(self, unique_id, user_id, product_name):
        self.unique_id = unique_id
        self.user_id = user_id
        self.product_name = product_name

def start() -> scoped_session:
    # engine = create_engine(DB_URI, client_encoding="utf8")
    # mysql: // user: pwd @ localhost / college
    engine = create_engine(f'sqlite:///test.db')
    # engine = create_engine(f'mysql://root:@localhost/apibot')
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    Broadcast.__table__.create(checkfirst=True, bind = engine)
    AddProduct.__table__.create(checkfirst=True, bind = engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


SESSION = start()

INSERTION_LOCK = threading.RLock()





# Broadcast.__table__.create(checkfirst=True)


class AddChannel(BASE):
    __tablename__ = "channel"

    unique_id = Column(String(50), primary_key=True)
    channel_id = Column(BigInteger)
    channel_name = Column(TEXT)
    user_id = Column(Numeric)
    batch = Column(TEXT)

    def __init__(self, unique_id, channel_id, channel_name, user_id, batch):
        self.unique_id = unique_id
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.user_id = user_id
        self.batch = batch



# AddChannel.__table__.create(checkfirst=True)


#  Add user details -
async def add_user(id, user_name):
    with INSERTION_LOCK:
        msg = SESSION.query(Broadcast).get(id)
        if not msg:
            usr = Broadcast(id, user_name)
            SESSION.add(usr)
            SESSION.commit()
        else:
            pass


async def add_channel(channel_id, channel_name, user_id, batch):
    with INSERTION_LOCK:
        # msg = SESSION.query(AddChannel.user_id).get(channel_id)
        try:
            msg = SESSION.query(AddChannel).filter_by(user_id=user_id, batch=batch, channel_id=channel_id).one()
            print("#################")
            print("obj", msg)
            print("#################")
            return "Already the channel is added in **"+batch+"** to this Bot. Please check!"

        except Exception as e:
            print("[Dina]Exception is : ", e)
            e = str(e)
            try:
                generated_unique_id = uuid.uuid1()
                print(generated_unique_id)
                channel = AddChannel(str(generated_unique_id), channel_id, channel_name, user_id, batch)
                SESSION.add(channel)
                SESSION.commit()
                return "Success"
            except Exception as e:
                print(e)
                return "Something went wrong while adding channel"

        # msg = SESSION.query(AddChannel.user_id).get(channel_id)
        # if not msg:
        #     channel = AddChannel(channel_id, channel_name, user_id)
        #     SESSION.add(channel)
        #     SESSION.commit()
        # else:
        #     print("channel may be added already or something may went wrong in sql.py")

async def add_product(user_id, product_name):
    print("in ")
    with INSERTION_LOCK:
        # msg = SESSION.query(AddChannel.user_id).get(channel_id)
        try:
            msg = SESSION.query(AddProduct).filter_by(user_id=user_id, product_name=product_name).one()
            print("#################")
            print("obj", msg)
            print("#################")
            return "Already the channel is added in **"+ product_name +"** to this Bot. Please check!"

        except Exception as e:
            print("[Dina]Exception is : ", e)
            #e = str(e)
            try:
                print("in Add Product")
                generated_unique_id = uuid.uuid1()
                print(generated_unique_id)
                product = AddProduct(str(generated_unique_id), user_id, product_name)
                SESSION.add(product)
                SESSION.commit()
                return "Success"
            except Exception as e:
                print(e)
                return "Something went wrong while adding channel"


# get info
async def full_userbase():
    users = SESSION.query(Broadcast).all()
    SESSION.close()
    return users

async def full_channelbase(user_id):
    channels = SESSION.query(AddChannel).filter_by(user_id=user_id)
    print("object", channels)
    SESSION.close()
    return channels

async def full_productbase(user_id):
    products = SESSION.query(AddProduct).filter_by(user_id=user_id).all()
    print("object", products)
    SESSION.close()
    return products

async def show_productbase_web(user_id):
    products = SESSION.query(AddProduct).filter_by(user_id=user_id).all()
    print("object", products)
    SESSION.close()
    return products

async def query_msg():
    try:
        query = SESSION.query(Broadcast.id).order_by(Broadcast.id)
        return query
    finally:
        SESSION.close()


async def channel_query_msg(user_id, batch):
    try:
        query = SESSION.query(AddChannel).filter_by(user_id=user_id, batch=batch)
        return query

    finally:
        SESSION.close()


#delete
async def delete_channel(channel_id, user_id, batch):
    # obj = SESSION.query(AddChannel.id).filter_by(id=channel_id)
    # print("object", obj[0].id)
    # obj = SESSION.query.filter_by(id=123).one()
    obj = SESSION.query(AddChannel).filter_by(user_id=user_id, channel_id=channel_id, batch=batch).one()
    # obj = SESSION.query(AddChannel).get(channel_id)
    print("#################")
    print("obj", obj)
    print("#################")
    SESSION.delete(obj)
    SESSION.commit()
    SESSION.close()

async def delete_batch(user_id, batch):

    obj = SESSION.query(AddChannel).filter_by(user_id=user_id, batch=batch).all()
    print("#################")
    print("obj", obj)
    for i in obj:
      SESSION.delete(i)
      
    print("#################")
    SESSION.commit()
    SESSION.close()