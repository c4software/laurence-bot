# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Text, Date, DateTime
from .custom_type import JsonEncodedDict

from database import Base
import datetime


class User(Base):
    __tablename__ = 'user'
    id_user = Column(Integer, primary_key=True)
    username = Column(Text)
    settings = Column(JsonEncodedDict)

    def __init__(self, iduser, username):
        if not username or not iduser:
            raise Exception("All fields are required")
        self.iduser = iduser
        self.username = username


class Historique(Base):
    __tablename__ = 'historique'
    id_historique = Column(Integer, primary_key=True)
    username = Column(Text)
    text = Column(Text)
    datetime = Column(DateTime)

    def __init__(self, username, text):
        if not username or not text:
            raise Exception("All field are required")

        self.username = username
        self.text = text
        self.datetime = datetime.datetime.today()


class Task(Base):
    __tablename__ = 'task'
    id_task = Column(Integer, primary_key=True)
    username = Column(Text)
    last_execution = Column(DateTime)
    planned_time = Column(String)
    commande = Column(Text)

    def __init__(self, username, planned_time, commande):
        if not username or not planned_time or not commande:
            raise Exception("All fields are required")

        self.username = username
        self.planned_time = planned_time
        self.commande = commande
        self.last_execution = datetime.today()

class MeetingReport(Base):
    __tablename__ = "meeting_report"
    id_report = Column(Integer, primary_key=True)
    date_report = Column(Date, default=datetime.date.today())
    user = Column(Text)
    team = Column(Text)
    data = Column(JsonEncodedDict)

    def __init__(self, user, team, data):
        self.user = user
        self.team = team
        self.data = data

class Learning_command(Base):
    __tablename__ = "learning_command"
    id_learn = Column(Integer, primary_key=True)
    tags_len = Column(Integer)
    tags = Column(JsonEncodedDict)
    commande = Column(Text)

    def __init__(self, tags, commande):
        self.tags = tags
        self.commande = commande
        self.tags_len = len(tags)


class Link(Base):
    __tablename__ = "links"
    id_links = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.date.today())
    link = Column(Text)
    channel = Column(Text)

    def __init__(self, link, channel):
        self.link = link
        self.channel  = channel