# -*- encoding=UTF-8 -*-
from photowall import app, db
from photowall.models import User, Image, Comment
from flask_script import Manager
import random

manage = Manager(app)

def get_image_url():
    return "http://images.nowcoder.com/head/" + str(random.randint(0, 1000)) + 't.png'

@manage.command
def init_database():
    db.drop_all()
    db.create_all()
    for i in range(100):
        db.session.add(User('User'+str(i), 'pwd'+str(i)))
        for j in range(0, 3):
            db.session.add(Image(get_image_url(), i + 1))
            for k in range(0, 3):
                db.session.add(Comment('This is comment' + str(k), 1+3*i+j, i + 1))
    db.session.commit()


if __name__ == '__main__':
    manage.run()
