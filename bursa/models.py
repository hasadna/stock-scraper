import peewee
from db import db


class DatabaseModel(peewee.Model):
    class Meta:
        database = db.database


class Company(DatabaseModel):
    id = peewee.PrimaryKeyField()
    name = peewee.CharField(unique=True, null=False)
    site_id = peewee.IntegerField(unique=True, null=False)
    description = peewee.CharField(null=True)
    website = peewee.CharField(null=True)
    email = peewee.CharField(null=True)
    corporate_number = peewee.CharField(null=True)
    issuer_number = peewee.IntegerField(null=True)
    industry = peewee.CharField(null=True)
    sector = peewee.CharField(null=True)
    niche = peewee.CharField(null=True)
    location = peewee.CharField(null=True)

class MarketCap(DatabaseModel):
    id = peewee.PrimaryKeyField()
    company = peewee.ForeignKeyField(Company)
    cap = peewee.IntegerField()

class StakeHolders(DatabaseModel):
    id = peewee.PrimaryKeyField()
    company = peewee.ForeignKeyField(Company)
    name = peewee.CharField()
    note = peewee.CharField(null=True)
    update_date = peewee.DateField()
    site = peewee.IntegerField(null=True)
    security_name = peewee.CharField(null=True)
    stock_count = peewee.IntegerField(null=True)
    capital_rate = peewee.FloatField(null=True)
    proxy_rate = peewee.FloatField(null=True)
    market_cap = peewee.FloatField(null=True)

class Management(DatabaseModel):
    id = peewee.PrimaryKeyField()
    company = peewee.ForeignKeyField(Company)
    name = peewee.CharField()
    position = peewee.CharField(null=True)
    security_name = peewee.CharField(null=True)
    stock_count = peewee.IntegerField(null=True)
    capital_rate = peewee.FloatField(null=True)
    proxy_rate = peewee.FloatField(null=True)
    expertise = peewee.BooleanField(null=True)
    audit_committee = peewee.BooleanField(null=True)

class FinancialReport(DatabaseModel):
    id = peewee.PrimaryKeyField()
    company = peewee.ForeignKeyField(Company)
    year = peewee.IntegerField(unique=True, null=False)
    total_balance = peewee.IntegerField(null=True)
    current_assets = peewee.IntegerField(null=True)
    long_term_assets = peewee.IntegerField(null=True)
    shareholders_equity = peewee.IntegerField(null=True)
    minority_equity = peewee.IntegerField(null=True)
    current_liabilities = peewee.IntegerField(null=True)
    long_term_liabilities = peewee.IntegerField(null=True)
    revenues = peewee.IntegerField(null=True)
    gross_profit = peewee.IntegerField(null=True)
    operating_income = peewee.IntegerField(null=True)
    income_before_tax = peewee.IntegerField(null=True)
    net_income = peewee.IntegerField(null=True)
    net_income_attributable_to_shareholders = peewee.IntegerField(null=True)
    net  = peewee.IntegerField(null=True)
    dividend = peewee.IntegerField(null=True)
    operating_activities_cash = peewee.IntegerField(null=True)
    capital_market = peewee.IntegerField(null=True)
    multiplier = peewee.IntegerField(null=True)
    capital_to_balance_sheet_ratio = peewee.IntegerField(null=True)
    return_on_equity = peewee.IntegerField(null=True)
