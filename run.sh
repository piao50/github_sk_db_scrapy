#!/usr/bin/env bash
# python -m pip install -r requirements.txt

cd skydb
scrapy crawl sk --logfile skydb.log --loglevel DEBUG
cd ..
