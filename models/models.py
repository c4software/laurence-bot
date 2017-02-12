# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Text, DateTime, TypeDecorator
from .custom_type import JsonEncodedDict

from database import Base
from datetime import datetime

class User(Base):
	__tablename__ 	= 'user'
	id_user		 	= Column(Integer, primary_key=True)
	username 		= Column(Text)
	settings		= Column(JsonEncodedDict)

	def __init__(self, iduser, username):
		if not username or not iduser:
			raise Exception("All fields are required")

		self.iduser 	= iduser
		self.username	= username

class Historique(Base):
	__tablename__ = 'historique'
	id_historique 	= Column(Integer, primary_key=True)
	username 		= Column(Text)
	text 			= Column(Text)
	datetime 		= Column(DateTime)

	def __init__(self, username, text):
		if not username or not text:
			raise Exception("All field are required")

		self.username 	= username
		self.text 		= text
		self.datetime	= datetime.today()

class Task(Base):
	__tablename__ 	= 'task'
	id_task		 	= Column(Integer, primary_key=True)
	username 		= Column(Text)
	last_execution 	= Column(DateTime)
	planned_time 	= Column(String)
	commande		= Column(Text)

	def __init__(self, username, planned_time, commande):
		if not username or not planned_time or not commande:
			raise Exception("All fields are required")

		self.username 		= username
		self.planned_time 	= planned_time
		self.commande 		= commande
		self.last_execution	= datetime.today()

class Learning_command(Base):
	__tablename__ 	= 	"learning_command"
	id_learn		= 	Column(Integer, primary_key=True)
	part_number		=	Column(Integer)
	tags	 		=	Column(JsonEncodedDict)
	commande	 	=	Column(Text)

	def __init__(self, tags, commande):
		self.tags 			=	tags
		self.commande		=	commande
		self.part_number	=	len(tags)
