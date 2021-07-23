# Etherscan_data_crawler
python crawler for url like https://cn.etherscan.com/token/0xf4cB3db185D11e1cD3eEFDe5FFA5dDF4976c3B2e
# manual
use `python crawl.py [token]`  
or `scrapy crawl escan -a url=[token]`  
such as `python crawl.py 0xf4cB3db185D11e1cD3eEFDe5FFA5dDF4976c3B2e`  
result output to .csv and mysql database described in pipelines.py
# new info.py
input a xlsx  
which consists of 8 columns, the 5th 6th 7th 8th column is  
from to quantitys method
**example: test.xlsx**
output info to the 9th column
