from operator import ne
from flask import Flask, render_template, flash, redirect, url_for, session
from flask_session import Session
from flask_login.utils import login_required
from form import user_registration, login, Property, landlord_form, tenant_form, tenant_login_form, landlord_login_form
from models import user, db, Properties, Landlord, Tenant, Unit
from flask_login import login_manager, login_user, logout_user, LoginManager
import datetime, random

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = ('mssql://KEVINKAGWIMA/sympatico?driver=sql server?trusted_connection=yes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkeythatyouarenotsupposedtosee'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'Landlord_login'
login_manager.login_message_category = "danger"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  return user.query.get(int(user_id))

@login_manager.user_loader
def load_user(Landlord_id):
  return Landlord.query.get(int(Landlord_id))

@login_manager.user_loader
def load_user(Tenant_id):
  return Tenant.query.get(int(Tenant_id))

active_users = []

@app.route("/")
@app.route("/home")
def index():
  return render_template('index.html')

@app.route("/registration", methods=["POST", "GET"])
def signup():
  form = user_registration()
  if form.validate_on_submit():
    date = datetime.datetime.now()
    member = user(
      first_name = form.first_name.data,
      second_name = form.second_name.data,
      last_name = form.last_name.data,
      email = form.email_address.data,
      phone = form.phone_number.data,
      date = date,
      username = form.username.data,
      passwords = form.password.data
      )
    db.session.add(member)
    db.session.commit()
    flash(f'User registered successfully', category='success')
    return redirect(url_for('signin'))
  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f'There was an error creating the user: {err_msg}', category='danger')

  return render_template('signup.html', form=form)

@app.route("/signin", methods=["POST", "GET"])
def signin():
  form = login()
  if form.validate_on_submit():
    member = user.query.filter_by(username=form.username.data).first()
    if member and member.check_password_correction(attempted_password=form.password.data):
      login_user(member)
      flash(f"Success! you are logged in: welcome {member.username}", category='success')
      return redirect(url_for('index'))
    else:
      flash(f"Invalid login credentials", category='danger')

  return render_template('signin.html', form=form)

@app.route("/logout")
def logout():
  logout_user()
  flash(f"Logged out successfully", category='success')
  return redirect(url_for('signin'))

@app.route("/landlord_registration", methods=["POST", "GET"])
def landlord():
  form = landlord_form()
  if form.validate_on_submit():
    new_landlord = Landlord(
      first_name = form.first_name.data,
      second_name = form.second_name.data,
      last_name = form.last_name.data,
      email = form.email_address.data,
      phone = form.phone_number.data,
      username = form.username.data,
      date = datetime.datetime.now(),
      landlord_id = random.randint(100000, 999999),
      passwords = form.password.data
    )
    db.session.add(new_landlord)
    db.session.commit()
    flash(f"Account created successfully", category="success")
    return redirect(url_for('Landlord_login'))
  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"There was an error creating the account: {err_msg}", category="danger")

  return render_template("landlord.html", form=form)

@app.route("/landlord_login", methods=["POST", "GET"])
def Landlord_login():
  form = landlord_login_form()
  new_landlord = Landlord.query.filter_by(landlord_id=form.landlord_id.data).first()
  if new_landlord and new_landlord.check_password_correction(attempted_password=form.password.data):
    login_user(new_landlord)
    flash(f"Authentication complete", category="success")
    properties = db.session.query(Properties).filter(new_landlord.id == Properties.owner)
    tenants = db.session.query(Tenant).filter(new_landlord.id == Tenant.landlord).all()
    active_users.append(new_landlord)
    return render_template('dashboard1.html', properties=properties, tenants=tenants)
  else:
    flash(f"Invalid credentials", category="danger")

  return render_template("landlord_login.html", form=form)

@app.route("/Landlord_dashboard", methods=["POST", "GET"])
@login_required
def landlord_dashboard():
  return render_template("dashboard1.html")

@app.route("/logout_landlord")
@login_required
def landlord_logout():
  logout_user()
  flash(f"Logged out successfully!", category="success")
  return redirect(url_for('Landlord_login'))

@app.route("/tenant_registration", methods=["POST", "GET"])
def tenant():
  form = tenant_form()
  if form.validate_on_submit():
    new_tenant = Tenant(
      first_name = form.first_name.data,
      second_name = form.second_name.data,
      last_name = form.last_name.data,
      email = form.email_address.data,
      phone = form.phone_number.data,
      username = form.username.data,
      date = datetime.datetime.now(),
      tenant_id = random.randint(100000, 999999),
      passwords = form.password.data,
      landlord = Landlord.query.filter_by(landlord_id=form.landlord_id.data).first().id
    )
    db.session.add(new_tenant)
    db.session.commit()
    login_user(new_tenant)
    flash(f"Account created successfully", category="success")
    return redirect(url_for('tenant_login'))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"There was an error creating the account {err_msg}", category="danger")

  return render_template("tenant.html", form=form)

@app.route("/tenant_authentication", methods=["POST", "GET"])
def tenant_login():
  form = tenant_login_form()
  if form.validate_on_submit():
    new_tenant = Tenant.query.filter_by(tenant_id=form.tenant_id.data).first()
    if new_tenant and new_tenant.check_password_correction(attempted_password=form.password.data):
      login_user(new_tenant)
      flash(f"Authentication complete", category="success")
      landlord = db.session.query(Landlord).filter(new_tenant.landlord == Landlord.id).first()
      return render_template('dashboard.html', landlord=landlord)
    else:
      flash(f"Invalid credentials", category="danger")

  return render_template("tenant_login.html", form=form)

@app.route("/logout_tenant")
def tenant_logout():
  logout_user()
  flash(f"Logged out successfully!", category="success")
  return redirect(url_for('tenant_login'))

@app.route("/Landlord_portal/property_registration", methods=["POST", "GET"])
@login_required
def property():
  form = Property()
  if form.validate_on_submit():
    new_property = Properties(
      name = form.name.data,
      address = form.Address.data,
      floors = form.floors.data,
      rooms = form.units.data,
      Type = form.Type.data,
      unique_id = random.randint(100000, 999999),
      date = datetime.datetime.now(),
      owner = Landlord.query.filter_by(landlord_id=form.landlord_id.data).first().id
    )
    db.session.add(new_property)
    db.session.commit()
    flash(f"Property: {new_property.name}  was created successfully", category='success')
    return redirect(url_for('landlord_dashboard'))
    
  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f'There was an error creating the property: {err_msg}', category='danger')

  return render_template("property.html", form=form)
  