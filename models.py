from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref, relationship
from flask_login import UserMixin


db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100), unique=True)


class Stamp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    # Just to make sure deleting a user also deletes the stamps
    user = relationship(User, backref=backref('Stamp', cascade='all,delete'))
    name = db.Column(db.String(100))
    year = db.Column(db.Integer)
    isPublic = db.Column(db.Boolean)
    fileName = db.Column(db.String(150))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    sender = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    receiver = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    # Just to make sure deleting a user also deletes the messages
    sender_r = relationship(User, backref=backref('Message sndr', cascade='all,delete'),
                            primaryjoin=User.id == sender)
    receiver_r = relationship(User, backref=backref('Message rcvr', cascade='all,delete'),
                              primaryjoin=User.id == receiver)
    content = db.Column(db.String(140))
    seen = db.Column(db.Boolean)


class Exchange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answered = db.Column(db.Boolean)
    accepted = db.Column(db.Boolean)
    senderID = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    receiverID = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    senderStampID = db.Column(db.Integer, db.ForeignKey('stamp.id', ondelete='CASCADE'))
    receiverStampID = db.Column(db.Integer, db.ForeignKey('stamp.id', ondelete='CASCADE'))
    # make sure we delete the exchange when stamps disappear
    MyStampID_r = relationship(Stamp, backref=backref('Exchange sndr', cascade='all,delete'),
                               primaryjoin=Stamp.id == senderStampID)
    OtherStampID_r = relationship(Stamp, backref=backref('Exchange rcvr', cascade='all,delete'),
                                  primaryjoin=Stamp.id == receiverStampID)
