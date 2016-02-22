SPIDER_MODULES = ['bursa.spiders']
DEFAULT_ITEM_CLASS = 'bursa.items.InfoItem'
ITEM_PIPELINES = {
    'bursa.pipelines.SaveInfoItemToDB': 1,
    'bursa.pipelines.SaveMarketCapItemToDB': 1,
    'bursa.pipelines.SaveStakeHolderItemsToDB': 1,
    'bursa.pipelines.SaveManagementItemsToDB': 1
}

DATABASE = {
    'class': 'MySQLDatabase',
    'name': 'bursa-test',
    'host': '',
    'user': 'root',
    'password': ''
}