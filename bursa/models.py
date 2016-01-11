import peewee
from db import db


class DatabaseModel(peewee.Model):
    class Meta:
        database = db.database


class Company(DatabaseModel):
    id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField(unique=True, null=False)
    site_id = peewee.IntegerField(unique=True, null=False)
    description = peewee.CharField()
    website = peewee.CharField()
    email = peewee.CharField()
    registrar_number = peewee.CharField()
    issuer_number = peewee.IntegerField()
    market = peewee.CharField()
    sector = peewee.CharField()
    sub_sector = peewee.CharField()
    location = peewee.CharField()

class MarketCap(DatabaseModel):
    id = peewee.IntegerField(primary_key=True)
    company = peewee.ForeignKeyField(Company)
    value = peewee.IntegerField()

class StakeHolders(DatabaseModel):
    id = peewee.IntegerField(primary_key=True)
    company = peewee.ForeignKeyField(Company)
    name = peewee.CharField()
    note = peewee.CharField()
    update_date = peewee.DateField()
    site = peewee.IntegerField()
    security_name = peewee.CharField()
    stock_count = peewee.IntegerField()
    capital_rate = peewee.FloatField()
    proxy_rate = peewee.FloatField()
    market_cap = peewee.FloatField()
