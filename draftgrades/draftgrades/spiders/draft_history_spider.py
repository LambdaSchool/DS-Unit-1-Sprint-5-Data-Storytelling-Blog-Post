import scrapy

class DraftHistorySpider(scrapy.Spider):
    name = "DraftHistory"
    def __init__(self):
        self.NFL_TEAMS = ['Cardinals',
        'Falcons',
        'Ravens',
        'Bills',
        'Panthers',
        'Bears',
        'Bengals',
        'Browns',
        'Cowboys',
        'Broncos',
        'Lions',
        'Packers',
        'Texans',
        'Colts',
        'Jaguars',
        'Chiefs',
        'Dolphins',
        'Vikings',
        'Patriots',
        'Saints',
        'Giants',
        'Jets',
        'Raiders',
        'Eagles',
        'Steelers',
        'Rams',
        'Chargers',
        '49ers',
        'Seahawks',
        'Buccaneers',
        'Titans',
        'Redskins']

    def start_requests(self):
        TEAMS = [x.lower() for x in self.NFL_TEAMS]
        for team in TEAMS:
            url = 'http://www.drafthistory.com/index.php/teams/{}'.format(team)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split('/')[-1]
        filename = 'draft-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)