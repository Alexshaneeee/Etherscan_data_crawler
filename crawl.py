import subprocess
import sys

if __name__ == "__main__":
    url = sys.argv[1]
    if url is not None:
        p = subprocess.Popen('scrapy crawl escan --nolog -a url=' + url, shell=True, stdout=sys.stdout)
        p.wait()
    else:
        url = '0xf4cB3db185D11e1cD3eEFDe5FFA5dDF4976c3B2e'
        p = subprocess.Popen('scrapy crawl escan --nolog ', shell=True, stdout=sys.stdout)
        p.wait()