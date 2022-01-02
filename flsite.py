import uuid

import bs4
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from part_time import Work_headers


class Site:
    """Represents object for a resource to scrape for job data"""
    job_headers = []

    def __init__(self, url, name, act_counter, suffs: [str], *containers, js=False):
        self.url = url
        self.name = name
        self.job_suffixes = suffs
        self.act_counter: int = act_counter
        self.html_cont = containers
        #possibly extensible for page mechanics check
        self.dyn = js

    #will be needed on added spec sufficcess
    def _url_constr(self, initial=True) -> str:
        """method for constructing spec urls with nuerations"""

        spec_url = self.url + self.job_suffixes[0]
        if not initial:
            return spec_url + self.job_suffixes[-1]
        return spec_url

    # def scrape_page(self):
    #     """hot jobs from first page"""
    #     scr_url = self._url_constr()
    #     init_sup = self._get_soup(scr_url)
    #     ziped_init = self._jobs_data(init_sup)
    #     self.ent_gen(ziped_init)

    def get_tasks(self):
        pass

    #needs to be combined with scrape_page
    def _jobs_data(self, soup):
        """getting html job info"""
        jh_parts = []
        for c, cl in self.html_cont:
            jh_parts.append(list(soup.find_all(c, cl)))
        fl_offrs = zip(*jh_parts)
        return fl_offrs

    #needs to be combined with scrape_page
    def scrape(self, needed=1):
        """getting offers from all but 1st page to list """
        _scr_counter = min(needed, self.act_counter)
        for c in range(_scr_counter):
            scr_url = self._url_constr(initial=False) + str(c)
            fl_sup = self._get_soup(scr_url)
            ziped_conts = self._jobs_data(fl_sup)
            self.ent_gen(ziped_conts)

    def ent_gen(self, parameters):
        """constructing job item for processing"""
        for jt, jp, jd in parameters:
            head = Work_headers(str(uuid.uuid4()), jt.text.strip(), jp.text.strip(),
                                jd.text.strip())
            self.job_headers.append(head)

    def _get_soup(self, url: str):
        """making soup object for of site"""

        def selenm_get(durl):
            """renders the scripted content"""
            chrome_opts = Options()
            chrome_opts.add_argument('--headless')
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_opts)
            driver.get(durl)
            return driver.page_source

        if self.dyn:
            page = selenm_get(url)
        else:
            page = requests.get(url)
        bs = bs4.BeautifulSoup(page.text, 'html.parser')
        return bs

    def show(self):
        for header in self.job_headers:
            print(header, end='\n')
