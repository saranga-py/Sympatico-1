from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SelectField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from models import Properties, user, Landlord, Tenant

class user_registration(FlaskForm):
  first_name = StringField(label='First Name', validators=[DataRequired()])
  second_name = StringField(label='Second Name', validators=[DataRequired()])
  last_name = StringField(label='Last Name', validators=[DataRequired()])
  email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
  phone_number = StringField(label='Phone number', validators=[Length(min=10, max=10, message="Invalid Phone Number"), DataRequired()])
  username = StringField(label='Username', validators=[Length(min=5, max=25), DataRequired()])
  password = PasswordField(label='Password', validators=[Length(min=5), DataRequired()])
  password1 = PasswordField(label='Confirm Password', validators=[EqualTo('password'), DataRequired()])

  def validate_username(self, username_to_validate):
    username = user.query.filter_by(username=username_to_validate.data).first()
    if username:
      raise ValidationError("Username already exists, Please try anotherone")

  def validate_phone_number(self, phone_number_to_validate):
    phone_number = user.query.filter_by(phone=phone_number_to_validate.data).first()
    if phone_number:
      raise ValidationError("Phone Number already exists, Please try another one")

  def validate_email_address(self, email_to_validate):
    email = user.query.filter_by(email=email_to_validate.data).first()
    if email:
      raise ValidationError("Email Address already exists, Please try another one")

class login(FlaskForm):
  username = StringField(label='Username', validators=[DataRequired()])
  password = PasswordField(label='Password', validators=[DataRequired()])

class landlord_form(FlaskForm):
  first_name = StringField(label='First Name', validators=[DataRequired()])
  second_name = StringField(label='Second Name', validators=[DataRequired()])
  last_name = StringField(label='Last Name', validators=[DataRequired()])
  email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
  phone_number = StringField(label='Phone number', validators=[Length(min=10, max=10, message="Invalid Phone Number"), DataRequired()])
  username = StringField(label="Username", validators=[Length(min=5, max=25), DataRequired()])
  password = PasswordField(label='Password', validators=[Length(min=5), DataRequired()])
  password1 = PasswordField(label='Confirm Password', validators=[EqualTo('password'), DataRequired()])

  def validate_phone_number(self, phone_number_to_validate):
    phone_number = Landlord.query.filter_by(phone=phone_number_to_validate.data).first()
    if phone_number:
      raise ValidationError("Phone Number already exists, Please try another one")

  def validate_email_address(self, email_to_validate):
    email = Landlord.query.filter_by(email=email_to_validate.data).first()
    if email:
      raise ValidationError("Email Address already exists, Please try another one")

class landlord_login_form(FlaskForm):
  landlord_id = IntegerField(label="Enter Landlord ID", validators=[DataRequired()])
  password = PasswordField(label="Enter Password", validators=[DataRequired()])

class tenant_form(FlaskForm):
  first_name = StringField(label='First Name', validators=[DataRequired()])
  second_name = StringField(label='Second Name', validators=[DataRequired()])
  last_name = StringField(label='Last Name', validators=[DataRequired()])
  email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
  phone_number = StringField(label='Phone number', validators=[Length(min=10, max=10, message="Invalid Phone Number"), DataRequired()])
  username = StringField(label="Username", validators=[Length(min=5, max=25), DataRequired()])
  landlord_id = IntegerField(label="Enter Landlord ID", validators=[DataRequired()])
  password = PasswordField(label='Password', validators=[Length(min=5), DataRequired()])
  password1 = PasswordField(label='Confirm Password', validators=[EqualTo('password'), DataRequired()])

  def validate_phone_number(self, phone_number_to_validate):
    phone_number = Tenant.query.filter_by(phone=phone_number_to_validate.data).first()
    if phone_number:
      raise ValidationError("Phone Number already exists, Please try another one")
  
  def validate_email_address(self, email_to_validate):
    email = Tenant.query.filter_by(email=email_to_validate.data).first()
    if email:
      raise ValidationError("Email Address already exists, Please try another one")

  def validate_landlord_id(self, landlord_id_to_validate):
    landlord = Landlord.query.filter_by(landlord_id=landlord_id_to_validate.data).first()
    if landlord is None:
      raise ValidationError("Invalid Landlord ID")

class tenant_login_form(FlaskForm):
  tenant_id = IntegerField(label="Enter Tenant ID", validators=[DataRequired()])
  password = PasswordField(label="Enter password", validators=[DataRequired()])

class Property(FlaskForm):
  landlord_id = IntegerField(label="Enter Landlord ID", validators=[DataRequired()])
  name = StringField(label="Enter Property Name", validators=[DataRequired()])
  Address = StringField(label="Enter Property Address", validators=[DataRequired()])
  floors = IntegerField(label="Enter Number of Floors", validators=[DataRequired()])
  units = IntegerField(label="Enter Total Number of rooms", validators=[DataRequired()])
  Type = SelectField(label="Enter type of property", choices=["Apartment", "Residential", "Office", "Warehouse"], validators=[DataRequired()])

  def validate_landlord_id(self, property_id_to_validate):
    landlord = Landlord.query.filter_by(landlord_id=property_id_to_validate.data).first()
    if landlord is None:
      raise ValidationError("Invalid Landlord ID")

class unit_form(FlaskForm):
  property_id = IntegerField(label="Enter Property ID", validators=[DataRequired()])
  name = StringField(label='Name of Unit', validators=[DataRequired()])
  floor = IntegerField(label='Floor', validators=[DataRequired()])
  quantity = IntegerField(label="Enter Quantity", validators=[DataRequired()])
  Type = SelectField(label='Type of Unit',choices=["1 Bedroom", "2 Bedroom", "3 Bedroom", "Bedsitter", "1 Bedroom", "Penthouse", "4 Bedroom", "Mansionate"], validators=[DataRequired()])
  tenant_id = IntegerField(label="Enter Tenant ID", validators=[DataRequired()])

  def validate_property_id(self, unit_id_to_validate):
    property = Properties.query.filter_by(property_id=unit_id_to_validate.data).first()
    if property is None:
      raise ValidationError("Invalid Property ID")

class complaint_form(FlaskForm):
  tenant_id = IntegerField(label="Enter Tenant ID", validators=[DataRequired()])
  title = StringField(label="Enter Title", validators=[Length(min=5, max=100), DataRequired()])
  category = SelectField(label="Choose A category", choices=["Electricity", "Water", "Repairs", "Other"], validators=[DataRequired()])
  body = TextAreaField(label="Type Complaint", validators=[DataRequired()])
