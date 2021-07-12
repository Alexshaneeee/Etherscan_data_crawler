# 如需调用此splash爬虫，请进入settings.py取消最后一段内容的注释
import scrapy
from scrapy_splash import SplashRequest

from etherscan.items import EtherscanItem

script = '''
function main(splash, args)
  splash:go(args.url)
  splash:wait(args.wait)
  splash:runjs("iframe = function(){ var f = document.getElementById('tokentxnsiframe');  return f.contentDocument.getElementsByTagName('table')[0].innerHTML; }")
  local result = splash:evaljs("iframe()")
  return result
end
'''
 

class SpSpider(scrapy.Spider):
    name = 'sp'
    allowed_domains = ['cn.etherscan.com']
    start_urls = ['https://cn.etherscan.com/token/0xf4cB3db185D11e1cD3eEFDe5FFA5dDF4976c3B2e']

    def start_requests(self):  # 获取SplashRequest
        url = self.start_urls[0]
        yield SplashRequest(url, callback=self.parse, endpoint='execute',
                            args={'lua_source': script, 'wait': 2})

    def parse(self, response):
        item = EtherscanItem()
        item["txn_hash"] = response.xpath(
            "//span[@class='hash-tag text-truncate myFnExpandBox_searchVal']/a/text()").getall()
        item["method_date"] = response.xpath("//tr/td/span/text()").getall()
        item["from_to"] = response.xpath("//a[@data-toggle='tooltip']/text()").getall()
        item["quantity"] = response.xpath("//tr/td/text()").getall()
        yield item
