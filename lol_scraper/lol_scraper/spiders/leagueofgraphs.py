import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


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

    def parse_profile(self, response):
        profile = response.css("h1.bg-black::text").get()

        rows = response.xpath("//table[contains(@class,'recentGamesTable')]//tr[td]")
        for row in rows:
            gamemode = row.css("div.gameMode::text").get()
            if not gamemode or "Soloqueue" not in gamemode:
                continue

            result = row.css("div.victoryDefeatText::text").get()
            if not result:
                continue

            winner = "team_1" if "Victory" in result else "team_2"

            team_1 = row.css(
                "div.summonerColumn:nth-of-type(1) img::attr(title)"
            ).getall()
            team_2 = row.css(
                "div.summonerColumn:nth-of-type(2) img::attr(title)"
            ).getall()

            yield {
                "player": profile,
                "winner": winner,
                "team_1": team_1,
                "team_2": team_2,
            }

    def parse_game(self, response):
        """
        ally comp = response.css("div.summonerColumn:nth-of-type(1)").get()
        enemy comp = response.css("div.summonerColumn:nth-of-type(2)").get()
        """
        yield {
            "game_url": response.url,
            "team_1": response.css(
                "div.summonerColumn:nth-of-type(1) div.summonerName::text"
            ).getall(),
            "team_2": response.css(
                "div.summonerColumn:nth-of-type(2) div.summonerName::text"
            ).getall(),
        }
