import scrapy


class LeagueofgraphsSpider(scrapy.Spider):
    name = "leagueofgraphs"
    allowed_domains = ["leagueofgraphs.com"]
    start_urls = ["https://www.leagueofgraphs.com/rankings/summoners/kr/"]

    def parse(self, response):
        pass
