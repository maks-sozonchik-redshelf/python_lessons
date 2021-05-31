import datetime

from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash

from flask_shorten.app import app
from flask_shorten.forms import LoginForm, RegisterForm
from flask_shorten.models import AllLinks, User


@app.route('/', methods=['POST', 'GET'])
def read_links():
    if request.method == 'GET':
        data_last = AllLinks.query.order_by(AllLinks.id.desc()).first()
        next_id = data_last.id + 1 if data_last else 1
        data = AllLinks.query.all()
        return render_template('index.html', data=data,
                               next_id=next_id, url=request.url, user=current_user)
    else:
        link1 = AllLinks.query.filter_by(origin_link=request.form['origin']). \
            first()
        link2 = AllLinks.query.filter_by(short_link=request.form['short']). \
            first()
        if link1:
            return render_template('success.html', result=1,
                                   link=link1, url=request.url), 400
        elif link2:
            return render_template('success.html', result=2,
                                   link=link2, url=request.url), 400
        else:
            if not request.form['short']:
                return render_template('success.html', result=5), 400
            else:
                link = AllLinks(origin_link=request.form['origin'],
                                short_link=request.form['short'],
                                date_create=datetime.datetime.now(),
                                counter=0)
                link.save()
                return render_template('success.html', result=3,
                                       link=link, url=request.url)


@app.route('/<string:end>')
def go_link(end=None):
    link = AllLinks.query.filter_by(short_link=end).first()
    if link:
        link.counter += 1
        link.save()
        return redirect(link.origin_link), 303
    else:
        return render_template('success.html', result=4, url=request.url), 404


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    if form.validate_on_submit():
        email = form.email.data
        psw = form.psw.data
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.hash_password, psw):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('profile'))

    return render_template('login.html', form=form), 400


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    if form.validate_on_submit():
        name = form.username.data
        email = form.email.data
        psw = generate_password_hash(form.psw.data)
        if User.query.filter(or_(User.name == name, User.email == email)).first():
            flash('user with email or name is used', category='error')
            return render_template('register.html', form=form), 400
        user = User(name=name, email=email, hash_password=psw)
        user.save()
        flash(f'user {name} was created', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form), 400


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('read_links'))
