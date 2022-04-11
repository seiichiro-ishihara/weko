# -*- coding: utf-8 -*-
#
# This file is part of WEKO3.
# Copyright (C) 2017 National Institute of Informatics.
#
# WEKO3 is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# WEKO3 is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WEKO3; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.

"""Pytest configuration."""
import os
import shutil
import tempfile
import json

import pytest
from flask import Flask, request, url_for
from flask_babelex import Babel
from invenio_db import InvenioDB, db
from invenio_accounts import InvenioAccounts
from invenio_accounts.testutils import create_test_user, login_user_via_session
from invenio_access import InvenioAccess
from invenio_access.models import ActionUsers
from invenio_indexer import InvenioIndexer
from invenio_search import InvenioSearch
from invenio_stats.config import SEARCH_INDEX_PREFIX as index_prefix
from simplekv.memory.redisstore import RedisStore
from sqlalchemy_utils.functions import create_database, database_exists, \
    drop_database

from weko_authors.views import blueprint_api
from weko_authors.models import Authors
from weko_authors import WekoAuthors
from weko_search_ui import WekoSearchUI


@pytest.yield_fixture()
def instance_path():
    """Temporary instance path."""
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path)


@pytest.fixture()
def base_app(instance_path, request):
    """Flask application fixture."""
    app_ = Flask('testapp', instance_path=instance_path)
    app_.config.update(
        SECRET_KEY='SECRET_KEY',
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=os.environ.get(
           'SQLALCHEMY_DATABASE_URI',
           'postgresql+psycopg2://invenio:dbpass123@postgresql:5432/invenio'),
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        INDEX_IMG='indextree/36466818-image.jpg',
        SEARCH_UI_SEARCH_INDEX='tenant1-weko',
    )
    Babel(app_)
    InvenioDB(app_)
    InvenioAccounts(app_)
    InvenioAccess(app_)
    InvenioIndexer(app_)
    InvenioSearch(app_)
    WekoAuthors(app_)
    WekoSearchUI(app_)
    _database_setup(app_, request)

    # app_.register_blueprint(blueprint)
    app_.register_blueprint(blueprint_api, url_prefix='/api/authors')
    return app_


@pytest.yield_fixture()
def app(base_app):
    """Flask application fixture."""
    with base_app.app_context():
        yield base_app


def _database_setup(app, request):
    """Set up the database."""
    with app.app_context():
        if not database_exists(str(db.engine.url)):
            create_database(str(db.engine.url))
        db.create_all()

    def teardown():
        with app.app_context():
            if database_exists(str(db.engine.url)):
                drop_database(str(db.engine.url))
            # Delete sessions in kvsession store
            if hasattr(app, 'kvsession_store') and \
                    isinstance(app.kvsession_store, RedisStore):
                app.kvsession_store.redis.flushall()

    request.addfinalizer(teardown)
    return app


@pytest.yield_fixture()
def client(app):
    """Get test client."""
    with app.test_client() as client:
        yield client


@pytest.fixture()
def users(app):
    """Create users."""
    ds = app.extensions['invenio-accounts'].datastore
    user = create_test_user(email='test@test.org')
    contributor = create_test_user(email='test2@test.org')
    comadmin = create_test_user(email='test3@test.org')
    repoadmin = create_test_user(email='test4@test.org')
    sysadmin = create_test_user(email='test5@test.org')

    r1 = ds.create_role(name='System Administrator')
    ds.add_role_to_user(sysadmin, r1)
    r2 = ds.create_role(name='Repository Administrator')
    ds.add_role_to_user(repoadmin, r2)
    r3 = ds.create_role(name='Contributor')
    ds.add_role_to_user(contributor, r3)
    r4 = ds.create_role(name='Community Administrator')
    ds.add_role_to_user(comadmin, r4)

    # Assign author-access to contributor, comadmin, repoadmin, sysadmin.
    with db.session.begin_nested():
        action_users = [
            ActionUsers(action='superuser-access', user=sysadmin),
            ActionUsers(action='author-access', user=contributor),
            ActionUsers(action='author-access', user=comadmin),
            ActionUsers(action='author-access', user=repoadmin)
        ]
        db.session.add_all(action_users)

    return [
        {'email': user.email, 'id': user.id,
         'password': user.password_plaintext, 'obj': user},
        {'email': contributor.email, 'id': contributor.id,
         'password': contributor.password_plaintext, 'obj': contributor},
        {'email': comadmin.email, 'id': comadmin.id,
         'password': comadmin.password_plaintext, 'obj': comadmin},
        {'email': repoadmin.email, 'id': repoadmin.id,
         'password': repoadmin.password_plaintext, 'obj': repoadmin},
        {'email': sysadmin.email, 'id': sysadmin.id,
         'password': sysadmin.password_plaintext, 'obj': sysadmin},
    ]


@pytest.fixture()
def id_prefix(client, users):
    """Create test prefix."""
    # login for create prefix
    login_user_via_session(client=client, email=users[4]['email'])

    input = {'name': 'testprefix', 'scheme': 'testprefix',
             'url': 'https://testprefix/##'}
    client.put('/api/authors/add_prefix',
               data=json.dumps(input),
               content_type='application/json')
    client.get(url_for('security.logout'))
