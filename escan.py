import re
import scrapy
from etherscan.items import EtherscanItem


class EscanSpider(scrapy.Spider):
    name = 'escan'
    allowed_domains = ['cn.etherscan.com']
    start_urls = ['https://cn.etherscan.com/token/0xf4cB3db185D11e1cD3eEFDe5FFA5dDF4976c3B2e']
    token = '0xf4cB3db185D11e1cD3eEFDe5FFA5dDF4976c3B2e'

    def __init__(self, url=None, *args, **kwargs):
        if url is not None:
            EscanSpider.token = url
            url = 'https://cn.etherscan.com/token/' + url
            self.start_urls = [url]
        super(EscanSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        url = self.start_urls[0]
        # yield scrapy.Request(url, callback=self.parse, meta={'proxy': "localhost:8888"}) #用于fiddler抓包
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, *args):
        json_str = response.xpath('//script[@type="text/javascript"]/text()').getall()
        str_all = ""
        for i in json_str:
            str_all = str_all + i
        sid = re.search('var sid = \'(.*)\'', str_all).group(1)
        addr = re.search('var litreadContractAddress = \'(.*)\'', str_all).group(1)
        i_url = 'https://cn.etherscan.com/token/generic-tokentxns2?m=normal&contractAddress=' + \
                addr + '&a=&sid=' + sid + '&p=1'
        # yield scrapy.Request(i_url, callback=self.iframe, meta={'proxy': "localhost:8888"}) #用于fiddler抓包
        yield scrapy.Request(i_url, callback=self.iframe)

    def iframe(self, response):
        item = EtherscanItem()
        item["txn_hash"] = response.xpath(
            "//span[@class='hash-tag text-truncate myFnExpandBox_searchVal']/a/text()").getall()
        item["method_date"] = response.xpath("//tr/td/span/@title").getall()
        item["from_to"] = []
        ft_list = response.xpath("//a[@data-toggle='tooltip']/@href").getall()
        for i in ft_list:
            m = re.search('a=(.*)', i)
            if m is not None:
                item["from_to"].append(m.group(1))
            else:
                item["from_to"].append(i)  # 错误保险
        item["quantity"] = response.xpath("//tr/td/text()").getall()
        item["token"] = EscanSpider.token
        yield item
