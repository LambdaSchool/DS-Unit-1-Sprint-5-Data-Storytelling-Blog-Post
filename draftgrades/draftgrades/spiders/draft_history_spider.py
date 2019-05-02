import scrapy
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

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

        self.path = '/Users/ridleyleisy/Documents/lambda/unit_one/DS-Unit-1-Sprint-5-Data-Storytelling-Blog-Post/draftgrades/'

    def start_requests(self):
        TEAMS = [x.lower() for x in self.NFL_TEAMS]
        for team in TEAMS:
            url = 'http://www.drafthistory.com/index.php/teams/{}'.format(team)
            yield scrapy.Request(url=url, callback=self.parse)
    
    def split_text(self, string):
        string = str(string)
        index_one = string.find('>')
        index_two = string.find('</')
        return string[index_one+1:index_two]

    def parse(self, response):
        page = response.url.split('/')[-1]
        filename = 'draft-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        html = open(self.path + filename)
        soup = BeautifulSoup(html,'html.parser')
        rows = soup.find("table", border=1).find_all("tr")
        rn = []
        t = []
        for row in rows[2:]:
            rn.append(row.find_all('td'))
        df = pd.DataFrame(rn)
        df.columns = ['year','no.','round','pick','player','name','position','college']
        for col in df.columns:
            df[col] = df[col].map(self.split_text)
        df['year'] = df['year'].replace('\xa0',np.nan).ffill()
        numeric_cols = ['no.','round','pick','player']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
        df.to_csv(filename+'.csv')