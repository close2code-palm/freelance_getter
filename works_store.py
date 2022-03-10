"""work store module
makes operations on database
and kind of DAO for scraped objects"""

from itertools import takewhile
from typing import Optional

import configparser
import psycopg2

from flsite import Site
from part_time import WorkHeaders


class StorageOperator:
    """makes all operations on database
    handles the connection and sql fuctionality
    gets data from Flsite instances"""

    def __init__(self, *stored: [Site]):
        # for st in stored:
        #     # some crazy manipulations before config
        #     self.strg = []
        #     fl_dict = {}
        #     scr_k, scr_dt = st.get_scraped()
        #     fl_dict[scr_k] = scr_dt
        #     self.strg.append(fl_dict)
        config = configparser.ConfigParser()
        config.read('db.ini')
        self.dsn = (
            f"host={config['postgresql']['host']}\
        user={config['postgresql']['user']} \
            password={config['postgresql']['passwd']} \
        port={config['postgresql']['port']} \
        database={config['postgresql']['db']}")

    # todo make update with 1 conection instead of 2
    def _get_watchers(self) -> Optional:
        """getting the most fresh row for each site
        possible """
        qry_names = '''CREATE or REPLACE VIEW jobs_on_sites_view AS 
            SELECT full_dscrptn, naming, timings 
            FROM fl_offers
            GROUP BY naming;'''
        qry = '''SELECT DISTINCT ON (naming) timings, naming, full_descrptn
            FROM fl_offers
            ORDER BY TIMESTAMP DESC
            LIMIT 1'''
        conn = psycopg2.connect(self.dsn)
        with conn:
            with conn.cursor() as crs:
                crs.execute(qry)
                latests = crs.fetchall()
        conn.close()
        return latests

    def update_in_db(self, whds: [WorkHeaders]):
        """Make write to db of new job data
        @:param whds is headers with same name"""
        query = f'''INSERT INTO fl_offers (uid, reward, full_dscrptn, timings, naming)
             VALUES (%s,%s,%s,%s,%s);'''

        def watcher_eqls(whdr: WorkHeaders):
            """possible repetetive fields,
            so checs 1+2 fields"""
            if (whdr.util_info, whdr.source, whdr.descr) in self._get_watchers():
                return True
            return False

        whds = takewhile(lambda x: watcher_eqls(x), whds)
        conn = psycopg2.connect(self.dsn)
        with conn:
            with conn.cursor() as crs:
                for header in whds:
                    crs.execute(query, (header.id, header.price,
                                        header.descr, header.util_info, header.source))
            conn.commit()
        conn.close()

class Storage:
    """Getting data for storing and sorting """

    def __init__(self):
        pass

    def sort(self):
        """Sorts items by key(ease, money, stack counts)"""

    def save(self):
        """Saves data in needed formats(database, model-files)"""