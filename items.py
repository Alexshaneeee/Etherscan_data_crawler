import scrapy


class EtherscanItem(scrapy.Item):
    txn_hash = scrapy.Field()
    method_date = scrapy.Field()
    from_to = scrapy.Field()
    quantity = scrapy.Field()
    token = scrapy.Field()
