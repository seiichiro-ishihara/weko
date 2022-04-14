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

import redis
from redis import sentinel
from flask import current_app
from simplekv.memory.redisstore import RedisStore

class RedisConnection:
    def __init__(self):
        self.redis_type = current_app.config['CACHE_TYPE']


    def connection(self, db, kv = False):
        datastore = None
        if self.redis_type == 'redis':
            store = self.redis_connection(db)
        elif self.redis_type == 'redissentinel':
            store = self.sentinel_connection(db)

        if kv == True:
            datastore = RedisStore(store)
        else:
            datastore = store

        return datastore

    def redis_connection(self, db):
        redis_url = current_app.config['CACHE_REDIS_HOST'] + ':' + current_app.config['REDIS_PORT'] + '/' + str(db)
        store = redis.StrictRedis.from_url(redis_url)

        return store

    def sentinel_connection(self, db):
        sentinels = sentinel.Sentinel(current_app.config['CACHE_REDIS_SENTINELS'], decode_responses=False)
        store = sentinels.master_for(
            current_app.config['CACHE_REDIS_SENTINEL_MASTER'], db= db)

        return store