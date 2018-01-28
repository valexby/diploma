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
                self.save_kernel_info(kernel)
            self.session.flush()
            self.session.commit()

    def save_kernel_info(self, kernel_json):
        msg = 'Try to process kernel id: {} lang: {} notebook: {} scr_id: {}'.format(kernel_json['id'],
                                                                                         kernel_json['aceLanguageName'],
                                                                                         kernel_json['isNotebook'],
                                                                                         kernel_json['scriptVersionId'])
        log.debug(msg)
        new_kernel = db.Kernel(id=kernel_json['id'],
                               title=kernel_json['title'])
        download_url = 'https://www.kaggle.com/kernels/sourceurl/{}'
        response = requests.get(download_url.format(kernel_json['scriptVersionId']))
        download_url = response.content.decode('utf-8')
        techs = self.get_technology(download_url,
                                    kernel_json['aceLanguageName'],
                                    kernel_json['isNotebook'])
        for tech in techs:
            rel = db.TechnologyRelation(technology=tech,
                                        kernel=new_kernel)
            self.session.add(rel)
        self.session.add(new_kernel)

    def get_technology(self, src_url, lang, notebook):
        script = os.path.join(basedir, 'get_tech.sh')
        script += ' \"{}\" \"{}\" \"{}\"'.format(src_url, lang, notebook)
        names = os.popen(script).read().split()
        old = self.session.query(db.Technology). \
              filter(db.Technology.title.in_(names)).all()
        old_names = [tech.title for tech in old]
        new_names = set(names) - set(old_names)
        new_tech = [db.Technology(title=title) for title in new_names]
        self.session.add_all(new_tech)
        return old + new_tech


    def run(self):
        self.get_kernels()
