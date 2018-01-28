#!/usr/bin/env python3
"""base_app for MediaLocker"""

import os
import requests

basedir, _ = os.path.split(__file__)

# logging
import logging, logging.config
log_config_file = os.path.join(basedir, 'logging.conf')
if os.path.exists(log_config_file):
    # load config from config file, see logging.conf for configuration settings
    logging.config.fileConfig(log_config_file)
else:
    # or just do a basic config
    format = '%(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s'
    logging.basicConfig(format=format, level=logging.NOTSET)

log = logging.getLogger(__package__)
log.debug("logging is setup")

import src.models as db
log.debug("db import")

class BaseApp():

    def __init__(self):
        log.debug('start init')

        db_driver = "mysql+pymysql"
        db_url = db.sa.engine.url.URL(db_driver,
                                      host='localhost',
                                      database='kaggle',
                                      username='root')
        log.debug("db: %s\n\n" % (db_url))

        log.debug("connect db")
        engine = db.sa.create_engine(db_url, echo=False)
        db.init_model(engine)
        self.session = db.db_session()

        log.debug("setup db")
        db.metadata.create_all(engine)
        log.debug("db created")

        self.newest_id = self.session.query(db.sa.func.max(db.Kernel.id)).first()[0]
        self.oldest_id = self.session.query(db.sa.func.min(db.Kernel.id)).first()[0]

        log.debug('end init')

    def get_kernels(self):
        TOKEN_LEN = 10
        params = {
            'sortBy': 'creation',
            'group': 'everyone',
            'pageSize': TOKEN_LEN,
        }
        new_models = []
        if self.newest_id:
            self.get_greatest(params, lambda x: x <= self.newest_id)
        else:
            self.get_greatest(params, lambda x: False)
        params['after'] = self.oldest_id
        if self.oldest_id:
            self.get_greatest(params, lambda x: x >= self.oldest_id)
        else:
            self.get_greatest(params, lambda x: False)

    def get_greatest(self, params, stop_condition):
        kernel_list_url = 'https://www.kaggle.com/kernels.json'
        kernels = []
        while True:
            response = requests.get(kernel_list_url, params)
            params['after'] = response.json()[-1]['id']
            for kernel in response.json():
                try:
                    kernel['title'].encode('latin-1')
                except UnicodeEncodeError:
                    continue
                if stop_condition(kernel['id']):
                    self.session.flush()
                    self.session.commit()
                    return
                kernels.append(self.save_kernel_info(kernel))
            self.session.flush()
            self.session.commit()

    def save_kernel_info(self, kernel_json):
        new_kernel = db.Kernel(id=kernel_json['id'],
                               title=kernel_json['title'])
        self session.add(new_kernel)
        return new_kernel

    def run(self):
        self.get_kernels()
