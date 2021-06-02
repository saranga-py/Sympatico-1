from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from sqlalchemy.orm import backref, lazyload

db = SQLAlchemy()
bcrypt = Bcrypt()

class user(db.Model, UserMixin):
  __tablename__ = "members"
  id = db.Column(db.Integer(), primary_key=True)
  first_name = db.Column(db.String(length=50), nullable=False)
  second_name = db.Column(db.String(length=50), nullable=False)
  last_name = db.Column(db.String(length=50), nullable=False)
  email = db.Column(db.String(length=100), nullable=False)
  phone = db.Column(db.Integer(), nullable=False)
  date = db.Column(db.DateTime())
  username = db.Column(db.String(length=50), nullable=False)
  password = db.Column(db.String, nullable=False)

  @property
  def passwords(self):
    return self.passwords

  @passwords.setter
  def passwords(self, plain_text_password):
    self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

  def check_password_correction(self, attempted_password):
    return bcrypt.check_password_hash(self.password, attempted_password)

class Landlord(db.Model, UserMixin):
  __tablename__ = "Landlord"
  id = db.Column(db.Integer(), primary_key=True)
  first_name = db.Column(db.String(length=50), nullable=False)
  second_name = db.Column(db.String(length=50), nullable=False)
  last_name = db.Column(db.String(length=50), nullable=False)
  email = db.Column(db.String(length=100), nullable=False)
  phone = db.Column(db.Integer(), nullable=False)
  username = db.Column(db.String(length=50), nullable=False)
  date = db.Column(db.DateTime())
  landlord_id = db.Column(db.Integer(), nullable=False)
  password = db.Column(db.String(), nullable=False)
  tenant = db.relationship('Tenant', backref="tenant", lazy=True)
  Property = db.relationship('Properties', backref="property", lazy=True)

  @property
  def passwords(self):
    return self.passwords

  @passwords.setter
  def passwords(self, plain_text_password):
    self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

  def check_password_correction(self, attempted_password):
    return bcrypt.check_password_hash(self.password, attempted_password)

class Tenant(db.Model, UserMixin):
  __tablename__ = "Tenant"
  id = db.Column(db.Integer(), primary_key=True)
  first_name = db.Column(db.String(length=50), nullable=False)
  second_name = db.Column(db.String(length=50), nullable=False)
  last_name = db.Column(db.String(length=50), nullable=False)
  email = db.Column(db.String(length=100), nullable=False)
  phone = db.Column(db.Integer(), nullable=False)
  username = db.Column(db.String(length=50), nullable=False)
  date = db.Column(db.DateTime())
  tenant_id = db.Column(db.Integer(), nullable=False)
  password = db.Column(db.String(), nullable=False)
  landlord = db.Column(db.Integer(), db.ForeignKey('Landlord.id'))
  unit = db.relationship('Unit', backref="unit", lazy=True)

  @property
  def passwords(self):
    return self.passwords

  @passwords.setter
  def passwords(self, plain_text_password):
    self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

  def check_password_correction(self, attempted_password):
    return bcrypt.check_password_hash(self.password, attempted_password)

class Properties(db.Model, UserMixin):
  __tablename__ = "Property"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(length=50), nullable=False)
  address = db.Column(db.String(length=100), nullable=False)
  floors = db.Column(db.Integer(), nullable=False)
  rooms = db.Column(db.Integer(), nullable=False)
  date = db.Column(db.DateTime())
  Type = db.Column(db.String(length=50), nullable=False)
  unique_id = db.Column(db.Integer(), nullable=False)
  owner = db.Column(db.Integer(), db.ForeignKey('Landlord.id'))
  unit = db.relationship('Unit', backref="units", lazy=True)

class Unit(db.Model, UserMixin):
  __tablename__ = "Unit"
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(length=50), nullable=False)
  floor = db.Column(db.Integer(), nullable=False)
  date = db.Column(db.DateTime())
  Type = db.Column(db.String(length=50), nullable=False)
  quantity = db.Column(db.Integer(), nullable=False)
  Property = db.Column(db.Integer(), db.ForeignKey('Property.id'))
  tenant = db.Column(db.Integer(), db.ForeignKey('Tenant.id'))
