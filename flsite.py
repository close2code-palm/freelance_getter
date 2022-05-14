"""Whole scrape machinery
class without threading
"""

import uuid

import bs4
import requests
from aiohttp import ClientSession
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from part_time import WorkHeaders, HabrWorkHeader


# Need to be splited into parser and site_handler
class Site:
    """Represents object for a resource to scrape for job data"""

    def get_scraped(self):
        return self.name, self.job_headers

    def __init__(self, url, name, act_counter,
                 suffs, *containers, js_rends=False):
        self.url = url
        self.name = name
        self.job_suffixes = suffs
        self.act_counter: int = act_counter
        self.html_cont = containers
        # TODO possibly extensible for page rendering mechanics check
        # if 'document.write' in ...
        self.dyn = js_rends
        # TODO store to not repeat
        # UNIQUE in db or watcher
        self.job_headers = []

    # will be needed on added spec sufficcess
    def _url_constr(self, sphere, initial=True) -> str:
        """method for constructing spec urls with nuerations"""

        spec_url = self.url + self.job_suffixes[sphere]
        if not initial:
            return spec_url + self.job_suffixes['pager']
        return spec_url

    # def scrape_page(self):
    #     """hot jobs from first page"""
    #     scr_url = self._url_constr()
    #     init_sup = self._get_soup(scr_url)
    #     ziped_init = self._jobs_data(init_sup)
    #     self.ent_gen(ziped_init)

    def get_tasks(self):
        pass

    def _jobs_data(self, soup):
        """getting html job info"""
        jh_parts = []
        for c, cl in self.html_cont:
            jh_parts.append(list(soup.find_all(c, cl)))
        fl_offrs = zip(*jh_parts)
        return fl_offrs

    def scrape(self, theme, needed=1):
        """getting offers from all but 1st page to list """
        # _scr_counter = min(needed, self.act_counter)
        last_sup = ""
        for c in range(1, needed + 1):
            # here MUST BE IMPLEMENTED CHECK FOR REPETITION
            scr_url = self._url_constr(theme, False) + str(c)
            fl_sup = self._get_soup(scr_url)
            # TODO returns function to thread? after check
            # possible sol: append(thread(args));excute;join

            if last_sup != fl_sup:
                ziped_conts = self._jobs_data(fl_sup)
                self.ent_gen(ziped_conts)
            else:
                break

    # TODO normalize utils
    def ent_gen(self, parameters):
        """constructing job item for processing"""
        for j_t, j_p, j_d in parameters:
            head = WorkHeaders(str(uuid.uuid4()), j_t.text.strip(), j_p.text.strip(),
                               j_d.text.strip(), self.name)
            self.job_headers.append(head)

    # TODO make decorator for concurrency
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
            btfl_sp = bs4.BeautifulSoup(page, 'html.parser')
        else:
            page = requests.get(url)
            btfl_sp = bs4.BeautifulSoup(page.text, 'html.parser')
        return btfl_sp

    # TODO should be moved to storage
    def show(self):
        for header in self.job_headers:
            print(self.name, header)


class HabrFlSite(Site):

    def __init__(self, url, name, act_counter,
                 suffs, *containers):
        super().__init__(url, name, act_counter,
                         suffs, *containers, js_rends=False)
        self.tags_lists = [('ul', {'class': 'tags_short'})]
        self.tags_concrete = 'a', {'class': 'tags__item_link'}
        self.tags_lists.extend(list(self.html_cont))
        self.html_cont = self.tags_lists


    def ent_gen(self, parameters):
        for tags_soup, j_t, j_p, j_d in parameters:
            tags = tags_soup.findall(*self.tags_concrete)
            habr_proposal = HabrWorkHeader(str(uuid.uuid4()),
                                           j_t.text.strip(), j_p.text.strip(),
                                           j_d.text.strip(), self.name,
                                           [tag.text for tag in tags])
            self.job_headers.append(habr_proposal)

