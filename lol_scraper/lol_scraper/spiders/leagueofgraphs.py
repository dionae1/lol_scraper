import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import LeagueOfGraphsItem, LeagueOfGraphsLoader


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
        rows = response.xpath("//table[contains(@class,'recentGamesTable')]//tr[td]")

        for row in rows:
            yield from self._extract_match(row)

    def _extract_match(self, row):
        match_id = row.css("a::attr(href)").get()
        match_id = match_id.split("/")[-1].split("#")[0] if match_id else None

        if not match_id or match_id in self.id_set:
            return

        self.id_set.add(match_id)

        gamemode = row.css("div.gameMode::text").get()
        if not gamemode or "Soloqueue" not in gamemode:
            return

        result = row.css("div.victoryDefeatText::text").get()
        player_won = result and "Victory" in result

        player_in_blue = bool(
            row.css("div.summonerColumn:nth-of-type(1) .selected img::attr(title)")
        )
        player_in_red = bool(
            row.css("div.summonerColumn:nth-of-type(2) .selected img::attr(title)")
        )

        if not (player_in_blue or player_in_red):
            winner = None
            print(f"Could not determine player's team for match {match_id}")
        else:
            if player_won:
                winner = "blue" if player_in_blue else "red"
            else:
                winner = "red" if player_in_blue else "blue"

        blue_team = row.css("div.summonerColumn:nth-of-type(1) img::attr(title)").getall()
        red_team = row.css("div.summonerColumn:nth-of-type(2) img::attr(title)").getall()

        loader = LeagueOfGraphsLoader(item=LeagueOfGraphsItem(), selector=row)
        loader.add_value("match_id", match_id)
        loader.add_value("winner", winner)
        loader.add_value("blue_team", blue_team)
        loader.add_value("red_team", red_team)

        yield loader.load_item()
