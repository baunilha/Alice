#################  import libraries ##########################

# -*- coding: utf-8 -*-
from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import * # for our custom signup form
from flask.ext.mongoengine.wtf.orm import validators
from flask.ext.mongoengine import *
from datetime import datetime


#################  create location and experience ##########################

class Location(mongoengine.Document):
	name = mongoengine.StringField(max_length=50)
	address = mongoengine.StringField()
	neighborhood = mongoengine.StringField(max_length=50)
	website = mongoengine.StringField(max_length=50)
	phone = mongoengine.StringField(max_length=50)

	# City, Price and hours are lists of Strings
	city = mongoengine.StringField(max_length=50)
	price = mongoengine.StringField()

	# Timestamp will record the date and time idea was created.
	timestamp = mongoengine.DateTimeField(default=datetime.now())


class Experience(mongoengine.Document):

	title = mongoengine.StringField(max_length=120, required=True, verbose_name="Experience")
	slug = mongoengine.StringField()
	description = mongoengine.StringField(max_length=500, verbose_name="Description")
	filename = mongoengine.StringField()
	
	# Period of the day and interest are lists of Strings
	period = mongoengine.ListField(mongoengine.StringField(max_length=30))
	interest = mongoengine.ListField(mongoengine.StringField(max_length=30))
	mood = mongoengine.ListField(mongoengine.StringField(max_length=30))

	location_refs = mongoengine.ListField( mongoengine.ReferenceField(Location))

	# Timestamp will record the date and time idea was created.
	timestamp = mongoengine.DateTimeField(default=datetime.now())

Experienceform = model_form(Experience)

# Create a WTForm form for the photo upload.
# This form will inhirit the Experience model above
# It will have all the fields of the Experience model
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


#################  create a new list ################################


class List(mongoengine.Document):
	user = mongoengine.ReferenceField('User', dbref=True) # ^^^ points to User model ^^^
	listName = mongoengine.StringField(max_length=50, required=True, verbose_name="Name of the List")
	slug = mongoengine.StringField()
	listDescription = mongoengine.StringField(max_length=500, verbose_name="Description")
	filename = mongoengine.StringField()
	timestamp = mongoengine.DateTimeField(default=datetime.now())
	experiences = mongoengine.ListField( mongoengine.ReferenceField(Experience) )

	city = mongoengine.ListField(mongoengine.StringField(max_length=50))

Listform = model_form(List)

# Create a WTForm form for the photo upload.
# This form will inhirit the List model above
# It will have all the fields of the List model
# We are adding in a separate field for the file upload called 'photoupload'
class photo_upload_list(Listform):
	photoupload = FileField('Upload an image file', validators=[])


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



	

