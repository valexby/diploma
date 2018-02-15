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
        db_url = str(db_url) + '?charset=utf8'
        log.debug("db: %s\n\n" % (db_url))

        log.debug("connect db")
        engine = db.sa.create_engine(db_url, echo=False)
        db.init_model(engine)
        self.session = db.db_session()

        log.debug("setup db")
        db.metadata.create_all(engine)
        log.debug("db created")

        log.debug('end init')

    def get_kernels(self):
        TOKEN_LEN = 10
        params = {
            'sortBy': 'creation',
            'group': 'everyone',
            'pageSize': TOKEN_LEN,
        }
        self.get_missing(params)

    def get_competitions(self):
        competitions_url = 'https://www.kaggle.com/competitions.json'
        PAGE_SIZE = 20
        params = {'sortBy': 'recentlyCreated',
                  'group': 'general',
                  'page': 1,
                  'pageSize': PAGE_SIZE,
        }
        response = requests.get(competitions_url, params)
        total_number = response.json()['pagedCompetitionGroup']['totalCompetitions']
        for page in range(1, (total_number // PAGE_SIZE) + 2):
            params['page'] = page
            response = requests.get(competitions_url, params)
            competitions = response.json()['pagedCompetitionGroup']['competitions']
            for competition in competitions:
                self.save_competition_info(competition)

    def save_competition_info(self, competition_json):
        TOKEN_LEN = 10
        competition = self.session.query(db.Competition).filter(db.Competition.id == competition_json['competitionId']).first()
        if not competition:
            competition = db.Competition(id=competition_json['competitionId'],
                                         title=competition_json['competitionTitle'])
            self.session.add(competition)
            self.session.flush()
            self.session.commit()
        params = {
            'sortBy': 'creation',
            'group': 'everyone',
            'pageSize': TOKEN_LEN,
            'competitionId': competition.id
        }
        self.get_missing(params)

    def get_missing(self, params):
        kernel_list_url = 'https://www.kaggle.com/kernels.json'
        while True:
            try:
                response = requests.get(kernel_list_url, params)
            except Exception as error:
                log_file = open('log.txt', "a")
                log_file.write("Crushed on GET {} with {} with {}".format(kernel_list_url,
                                                                          params,
                                                                          error))
                log_file.write('Exception: {}\n'.format(type(error)))
                log_file.close()
                continue
            if not response.json():
                return
            params['after'] = response.json()[-1]['id']
            for kernel in response.json():
                db_kernel = self.session.query(db.Kernel).filter(db.Kernel.id == kernel['id']).first()
                competition_id = None
                if db_kernel and db_kernel.source_version != kernel['scriptVersionId']:
                    competition_id = db_kernel.competition_id
                    self.session.delete(db_kernel)
                    db_kernel = None
                if not db_kernel:
                    newbie = self.save_kernel_info(kernel)
                    if not competition_id is None:
                        newbie.competition_id = competition_id
                    elif 'competitionId' in params:
                        newbie.competition_id = params['competitionId']
            self.session.flush()
            self.session.commit()

    def save_kernel_info(self, kernel_json):
        log_msg = 'Try to process kernel id: {} lang: {} notebook: {} scr_id: {}'
        log_msg = log_msg.format(kernel_json['id'],
                                 kernel_json['aceLanguageName'],
                                 kernel_json['isNotebook'],
                                 kernel_json['scriptVersionId'])
        log.debug(log_msg)
        new_kernel = db.Kernel(id=kernel_json['id'],
                               title=kernel_json['title'],
                               lang=kernel_json['aceLanguageName'],
                               notebook=kernel_json['isNotebook'],
                               votes=kernel_json['totalVotes'],
                               best_score=kernel_json['bestPublicScore'],
                               source_version=kernel_json['scriptVersionId'])
        download_url = 'https://www.kaggle.com/kernels/sourceurl/{}'
        download_url = download_url.format(new_kernel.source_version)
        try:
            response = requests.get(download_url)
            download_url = response.content.decode('utf-8')
            techs = self.get_technology(download_url,
                                        new_kernel.lang,
                                        new_kernel.notebook)
            for tech in techs:
                rel = db.TechnologyRelation(technology=tech,
                                            kernel=new_kernel)
                self.session.add(rel)
        except Exception as error:
            log_file = open('log.txt', "a")
            log_file.write(log_msg + ' ')
            log_file.write("Crushed on GET {} with {}\n".format(download_url, error))
            log_file.write('Exception: {}\n'.format(type(error)))
            log_file.close()
        cats = self.get_categories(kernel_json)
        for cat in cats:
            rel = db.CategoryRelation(category=cat,
                                      kernel=new_kernel)
            self.session.add(rel)
        data_links = self.get_data_link(kernel_json)
        for link in data_links:
            rel = db.DataLinkRelation(data_link=link,
                                      kernel=new_kernel)
            self.session.add(rel)
        self.session.add(new_kernel)
        return new_kernel

    def get_categories(self, kernel):
        cat_dict = {cat['name'] : cat for cat in kernel['categories']['categories']}
        if not cat_dict:
            return []
        old = self.session.query(db.Category). \
              filter(db.Category.title.in_(cat_dict.keys())).all()
        old_names = {cat.title for cat in old}
        new_names = set(cat_dict.keys()) - old_names
        new_categories = []
        for name in new_names:
            cat = cat_dict[name]
            new_categories.append(db.Category(title=cat['name'],
                                              description=cat['description']))
        self.session.add_all(new_categories)
        return new_categories + old

    def get_technology(self, src_url, lang, notebook):
        script = os.path.join(basedir, 'get_tech.sh')
        script += ' \"{}\" \"{}\" \"{}\"'.format(src_url, lang, notebook)
        names = os.popen(script).read().split()
        if not names:
            return names
        old = self.session.query(db.Technology). \
              filter(db.Technology.title.in_(names)).all()
        old_names = [tech.title for tech in old]
        new_names = set(names) - set(old_names)
        new_tech = [db.Technology(title=title) for title in new_names]
        self.session.add_all(new_tech)
        return old + new_tech

    def get_data_link(self, kernel):
        src_dict = {src['name'] : src for src in kernel['dataSources']}
        if not src_dict:
            return []
        old = self.session.query(db.DataLink). \
              filter(db.DataLink.title.in_(src_dict.keys())).all()
        old_names = {src.title for src in old}
        new_names = set(src_dict.keys()) - old_names
        new_data_links = []
        for name in new_names:
            src = src_dict[name]
            new_data_links.append(db.DataLink(title=src['name'],
                                              link=src['url']))
        self.session.add_all(new_data_links)
        return new_data_links + old

    def run(self):
        # self.get_kernels()
        self.get_competitions()
