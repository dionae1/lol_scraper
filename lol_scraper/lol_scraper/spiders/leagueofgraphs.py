import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from lol_scraper.items import LeagueOfGraphsItem


class LeagueofgraphsSpider(CrawlSpider):
    name = "leagueofgraphs"
    allowed_domains = ["leagueofgraphs.com"]
    start_urls = ["https://www.leagueofgraphs.com/rankings/summoners/kr/"]

    custom_settings = {
        "CONCURRENT_REQUESTS": 32,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 16,
        "CONCURRENT_REQUESTS_PER_IP": 0,
        "DOWNLOAD_DELAY": 0,
        "AUTOTHROTTLE_ENABLED": False,
        "COOKIES_ENABLED": False,
        "HTTPCACHE_ENABLED": True,
        "RETRY_TIMES": 1,
        "REDIRECT_ENABLED": True,
    }
    rules = (
        # get trough all ranking pages
        # Rule(
        #     LinkExtractor(allow=r"/page"),
        # ),
        Rule(
            LinkExtractor(allow=r"/summoner\/kr\/.+"),
            callback="parse_profile",
        ),
    )

    def __init__(self):
        super().__init__()
        self.id_set = set()

    def parse_profile(self, response):
        profile_name = response.css("h1.bg-black::text").get()
        rows = response.xpath("//table[contains(@class,'recentGamesTable')]//tr[td]")

        for row in rows:
            match_id = row.css("a::attr(href)").get()
            match_id = match_id.split("/")[-1].split("#")[0] if match_id else None

            if not match_id or match_id in self.id_set:
                continue

            self.id_set.add(match_id)

            gamemode = row.css("div.gameMode::text").get()
            if not gamemode or "Soloqueue" not in gamemode:
                continue

            result = row.css("div.victoryDefeatText::text").get()
            winner = "team_1" if "Victory" in result else "team_2"

            team_1 = row.css(
                "div.summonerColumn:nth-of-type(1) img::attr(title)"
            ).getall()
            team_2 = row.css(
                "div.summonerColumn:nth-of-type(2) img::attr(title)"
            ).getall()

            loader = ItemLoader(item=LeagueOfGraphsItem(), selector=row)
            loader.add_value("match_id", match_id)
            loader.add_value("winner", winner)
            loader.add_value("team_1", team_1)
            loader.add_value("team_2", team_2)

            yield loader.load_item()
