# How to Setup a crawler for www.dygod.net

## Quick setup

reference [here](http://doc.scrapy.org/en/latest/topics/commands.html?highlight=template#genspider)

    scrapy startproject scrapy_dygod
    cd scrapy_dygod
    scrapy genspider -l
    scrapy genspider -t crawl crawler_dygod www.dygod.net


Now go ahead and make some modifications to 

1. items.py
1. spider/crawler_dygod.py
1. pipelines.py

## Run the crawler

scrapy crawl crawler_dygod -o result.json
