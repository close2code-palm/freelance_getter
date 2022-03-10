import configparser
import psycopg2

from flsite import Site
from part_time import WorkHeaders


class Storage():

    def __init__(self, *stored: [Site]):
        for st in stored:
            # some crazy manipulations before config
            self.strg = []
            fl_dict = {}
            scr_k, scr_dt = st.get_scraped()
            fl_dict[scr_k] = scr_dt
            self.strg.append(fl_dict)
            config = configparser.ConfigParser()
            config.read('db.ini')
            self.DSN = (
                f"host={config['postgresql']['host']}\
            user={config['postgresql']['user']} \
                password={config['postgresql']['passwd']} \
            port={config['postgresql']['port']} \
            database={config['postgresql']['db']}")

        def _get_watcher(self):
            qury = '''SELECT full_dscrptn 
        FROM 
        ORDER BY TIMESTAMP DESC
  LILIMIT 1'''
            pass

        def update_in_db(self, whds: [WorkHeaders]):
            query = f'''INSERT INTO fl_offers (uid, reward, full_dscrptn, timings, naming)
                 VALUES (%s,%s,%s,%s,%s);'''
            conn = psycopg2.connect(self.DSN)
            with conn:
                with conn.cursor() as crs:
                    for header in whds:
                        crs.execute(query, (header.id, header.price,
                                            header.descr, header.util_info, header.source))
                conn.commit()
            conn.close()
