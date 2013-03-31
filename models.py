# -*- coding: utf-8 -*-
from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import * # for our custom signup form
from flask.ext.mongoengine.wtf.orm import validators
from flask.ext.mongoengine import *
from datetime import datetime

class Comment(mongoengine.EmbeddedDocument):
	name = mongoengine.StringField()
	comment = mongoengine.StringField()
	timestamp = mongoengine.DateTimeField(default=datetime.now())

class Location(mongoengine.EmbeddedDocument):
	name = mongoengine.StringField(max_length=50)
	address = mongoengine.StringField()
	neighborhood = mongoengine.StringField(max_length=50)
	website = mongoengine.StringField(max_length=50)
	phone = mongoengine.StringField(max_length=50)

	# City, Price and hours are lists of Strings
	city = mongoengine.ListField(mongoengine.StringField(max_length=50))
	price = mongoengine.ListField(mongoengine.StringField(max_length=20))
	hourOpen = mongoengine.ListField(mongoengine.StringField(max_length=20))
	hourClose = mongoengine.ListField(mongoengine.StringField(max_length=20))

	# Timestamp will record the date and time idea was created.
	timestamp = mongoengine.DateTimeField(default=datetime.now())

class Experience(mongoengine.Document):

	title = mongoengine.StringField(max_length=120, required=True, verbose_name="Experience")
	slug = mongoengine.StringField()
	description = mongoengine.StringField(max_length=500, verbose_name="Description")
	postedby = mongoengine.StringField(max_length=120, verbose_name="Your name")
	
	# Period of the day and interest are lists of Strings
	period = mongoengine.ListField(mongoengine.StringField(max_length=30))
	interest = mongoengine.ListField(mongoengine.StringField(max_length=30))

	filename = mongoengine.StringField()

	# Location is an embedded element
	locations = mongoengine.ListField( mongoengine.EmbeddedDocumentField(Location) )
	
	# Comments is a list of Document type 'Comments' defined above
	comments = mongoengine.ListField( mongoengine.EmbeddedDocumentField(Comment) )

	# Timestamp will record the date and time idea was created.
	timestamp = mongoengine.DateTimeField(default=datetime.now())

Experienceform = model_form(Experience)

# Create a WTForm form for the photo upload.
# This form will inhirit the Photo model above
# It will have all the fields of the Photo model
# We are adding in a separate field for the file upload called 'fileupload'
class photo_upload_form(Experienceform):
	fileupload = FileField('Upload an image file', validators=[])



	

