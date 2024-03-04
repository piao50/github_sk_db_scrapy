import scrapy
from scrapy.selector import Selector
from pathlib import Path
import os

OUTPUT = "../data/"
INDEX = "index.txt"
BGN = 1
END = 5858 + 1
# END = 3

class SkSpider(scrapy.Spider):
  name = 'sk'
  def start_requests(self):
    with Path(INDEX).open('r') as fp:
      lines = [int(line) for line in fp.readlines()]
      ids_fetched = set(lines)
    print(ids_fetched)

    for i in range(BGN, END):
      url = "http://fz.people.com.cn/skygb/sk/index.php/index/seach/{}/".format(i)
      if i in ids_fetched:
        self.log(f"{url} OMIT!")
      else:
        self.log(f"{url}")
        yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    page = response.url.split("/")[-2]
    filename = f"{OUTPUT}{int(int(page) / 100)}/sk-{page}.html"
    Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
    Path(filename).write_bytes(response.body)
    self.log(f"Saved file {filename}")
    with Path(INDEX).open('a') as fp:
      fp.write(f"{page}\r\n")

    result = []
    for row in response.selector.xpath("/html/body/div[3]/table/tr/td[2]/div/div/table//tr").getall():
      titles = []
      for title in Selector(text=row).xpath("//td/span/text()").getall():
        titles.append(title)
      if len(titles) > 0:
        result.append(','.join(titles))
    Path(filename + ".txt").write_text("\r\n".join(result))
