# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'ZH75GPXTK5T87S5BAJ6JU2QGZJWRDFBGC2HSPPIX'

######################
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repostory')
