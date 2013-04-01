#################  import libraries ##########################

# -*- coding: utf-8 -*-
from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import * # for our custom signup form
from flask.ext.mongoengine.wtf.orm import validators
from flask.ext.mongoengine import *
from datetime import datetime


#################  comments - not using ##########################

class Comment(mongoengine.EmbeddedDocument):
	name = mongoengine.StringField()
	comment = mongoengine.StringField()
	timestamp = mongoengine.DateTimeField(default=datetime.now())


#################  create location and experience ##########################

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


#######################  user models/forms ##########################

class User(mongoengine.Document):
	username = mongoengine.StringField(unique=True, max_length=30, required=True, verbose_name="Pick a Username")
	email = mongoengine.EmailField(unique=True, required=True, verbose_name="Email Address")
	password = mongoengine.StringField(default=True,required=True)
	active = mongoengine.BooleanField(default=True)
	isAdmin = mongoengine.BooleanField(default=False)
	timestamp = mongoengine.DateTimeField(default=datetime.now())

user_form = model_form(User, exclude=['password'])

# Signup Form created from user_form
class SignupForm(user_form):
	password = PasswordField('Password', validators=[validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')

# Login form will provide a Password field (WTForm form field)
class LoginForm(user_form):
	password = PasswordField('Password',validators=[validators.Required()])


###################  end of user models/forms ##########################


class Content(mongoengine.Document):
    user = mongoengine.ReferenceField('User', dbref=True) # ^^^ points to User model ^^^
    title = mongoengine.StringField(max_length="100",required=True)
    content = mongoengine.StringField(required=True)
    timestamp = mongoengine.DateTimeField(default=datetime.now())

    @mongoengine.queryset_manager
    def objects(doc_cls, queryset):
    	return queryset.order_by('-timestamp')

# content form
content_form = model_form(Content)



	

