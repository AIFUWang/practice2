# -*- encoding=UTF-8 -*-
from photowall import app, db
from photowall import models as md
from flask import render_template, redirect, request, flash, get_flashed_messages
import random, hashlib


@app.route('/')
def index():
    images = md.Image.query.order_by(db.desc(md.Image.id)).limit(10).all()
    return render_template('index.html', images=images)


@app.route('/image/<int:image_id>/')
def image(image_id):
    image = md.Image.query.get(image_id)
    if image == None:
        return redirect('/')
    return render_template('pageDetail.html', image=image)


@app.route('/profile/<int:user_id>/')
def profile(user_id):
    user = md.User.query.get(user_id)
    if user == None:
        return redirect('/')
    return render_template('profile.html', user=user)

@app.route('/regloginpage/')
def regloginpage():
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['relogin']):
        msg = msg + m
    return render_template('login.html', msg=msg)

def redirect_with_msg(target, msg, category):
    if msg !=None:
        flash(msg, category=category)
    return redirect(target)


@app.route('/reg/', methods={'post','get'})
def reg():
    #request.args
    #request.form
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    if username =='' or password == '':
        return redirect_with_msg('/regloginpage/', u'用户名或密码不能为空', 'reglogin')

    user = md.User.query.filter_by(username=username).first()
    if user != None:

        return redirect_with_msg('/regloginpage/', u'用户名已存在', 'reglogin')


    #更多判断

    salt = ''.join(random.sample('0123456789abcdefghijklmnABCDEFGHIJKLMN',6))
    m = hashlib.md5()
    m.update((password+salt).encode())
    password = m.hexdigest()
    user = md.User(username, password, salt)
    db.session.add(user)
    db.session.commit()
    return redirect('/')