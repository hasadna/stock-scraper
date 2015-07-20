SPIDER_MODULES = ['bursa.spiders']
DEFAULT_ITEM_CLASS = 'bursa.items.CompanyItem'
ITEM_PIPELINES = {'bursa.pipelines.SaveToFile': 1}
