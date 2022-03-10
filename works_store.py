from itertools import takewhile

import configparser
import psycopg2

from flsite import Site
from part_time import WorkHeaders


class Storage:

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

    def _get_watcher(self):
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
        query = f'''INSERT INTO fl_offers (uid, reward, full_dscrptn, timings, naming)
             VALUES (%s,%s,%s,%s,%s);'''

        def watcher_eqls(whdr: WorkHeaders):
            if (whdr.util_info, whdr.source, whdr.descr) in self._get_watcher():
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
