import scrapy
from Volleyball.items import ItemTeam, ItemSesson, ItemStatistic
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
        
class VolleyballSpiderSpider(scrapy.Spider):

    name = 'Volleyball_spider'
    allowed_domains = ['www.plusliga.pl']
    start_urls = ['https://www.plusliga.pl/statsTeams/tournament_1/all.html']
    limit = True

    def parse(self, response): # First parser, extracting teams present in all seassons, passing information to seasson parser
        for x in response.css('div.thumbnail.player.team-logo'):
            l = ItemLoader(item = ItemTeam(), selector=x)

            l.add_css('team_name', 'div h3 a::text')
            l.add_css('link', 'div h3 a::attr(href)')

            loaded = l.load_item()

            yield response.follow(loaded['link'], callback=self.parse_sessons, cb_kwargs=dict(team_name=loaded['team_name']))

    def parse_sessons(self, response, team_name): # Second parser, extracting seassons in which given team had at least 1 game, passing to table extractor

        l = ItemLoader(item = ItemSesson(), selector=response)

        l.add_xpath('sesson', "//a[contains(text(), 'Sezon')]/text()")
        l.add_xpath('link', "//a[contains(text(), 'Sezon')]/@href")
        loaded = l.load_item()

        for sesson, link in zip(loaded['sesson'], loaded['link']):

            yield response.follow(link, callback=self.parse_statistics, cb_kwargs=dict(team_name=team_name, sesson=sesson))
    
    def parse_statistics(self, response, team_name, sesson): # Last parser, from given seasson and team it extracts information stored in html table and pass it through pipeline

        l = ItemLoader(item=ItemStatistic())
        l.add_value('data', response.css('table.rs-standings-table.stats-table.table.table-bordered.table-hover.table-condensed.table-striped.responsive.double-responsive').get())
        l.add_value('team_name', team_name)
        l.add_value('sesson', sesson)
        l.add_value('limit', self.limit)
        yield l.load_item()
