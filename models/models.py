# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Text, DateTime, TypeDecorator
from .custom_type import JsonEncodedDict

from database import Base
from datetime import datetime

class User(Base):
	__tablename__ 	= 'user'
	iduser		 	= Column(Integer, primary_key=True)
	username 		= Column(Text)

	def __init__(self, iduser, username):
		if not username or not iduser:
			raise Exception("All field are required")

		self.iduser 	= iduser
		self.username	= username

class Historique(Base):
	__tablename__ = 'historique'
	idhistorique 	= Column(Integer, primary_key=True)
	username 		= Column(Text)
	text 			= Column(Text)
	datetime 		= Column(DateTime)

	def __init__(self, username, text):
		if not username or not text:
			raise Exception("All field are required")

		self.username 	= username
		self.text 		= text
		self.datetime	= datetime.today()

	def __repr__(self):
		return '<Historique %r>' % (self.idhistorique)

class Learning_command(Base):
	__tablename__ 	= 	"learning_command"
	idLearn		 	= 	Column(Integer, primary_key=True)
	username	 	= 	Column(Text)
	part_number		=	Column(Integer)
	tags	 		=	Column(JsonEncodedDict)
	commande	 	=	Column(Text)

	def __init__(self, username, tags, commande):
		self.username 		= 	username
		self.text 			=	tags
		self.commande		=	commande
