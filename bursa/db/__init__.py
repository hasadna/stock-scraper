import peewee
from bursa import settings


class Database(object):
    def __init__(self, db_properties):
        db_settings = dict(db_properties)
        db_name = db_settings.pop('name')
        db_class_name = db_settings.pop('class')
        db_class = getattr(peewee, db_class_name)
        self.database = db_class(db_name, **db_settings)
        self.app = None

    def init_app(self, app):
        self.app = app
        if app is not None:
            self.app.before_request(self.connect)
            self.app.teardown_request(self.close)

    def connect(self):
        self.database.connect()

    def close(self, exc):
        self.database.close()


db = Database(settings.DATABASE)