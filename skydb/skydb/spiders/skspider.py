import scrapy
from pathlib import Path
import os

OUTPUT = "../data/"

class SkSpider(scrapy.Spider):
  name = 'sk'
  def start_requests(self):
    urls = [
      "http://fz.people.com.cn/skygb/sk/index.php/index/seach/1/",
      "http://fz.people.com.cn/skygb/sk/index.php/index/seach/2/",
    ]
    for url in urls:
      yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    page = response.url.split("/")[-2]
    filename = f"{OUTPUT}{int(int(page) / 100)}/sk-{page}.html"
    Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
    Path(filename).write_bytes(response.body)
    self.log(f"Saved file {filename}") 

    item = response.selector.xpath("/html/body/div[3]/table/tbody/tr/td[2]/div/div/table/tbody/tr[1]").get()
    self.log(f"item : {item}") 
