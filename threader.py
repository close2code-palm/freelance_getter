import multiprocessing
import queue
import threading
from time import sleep

from flsite import Site


class Scanner:

    def __init__(self, page_deep, *sites, max_threads=4):
        self.resources: [Site] = sites
        self.qu = queue.Queue(max_threads)
        self.pages_tos = page_deep

    def thread_function(self, site_i):
        self.qu.put(site_i.scrape(self.pages_tos), site_i.show())

    def runner_h(self):
        # tq = queue.Queue(self.threads)
        thrds = []
        waiting_time = 0
        for site in self.resources:
            while self.qu.full():
                if waiting_time > 15:
                    raise TimeoutError
                waiting_time += 1
                sleep(1)
            #Should create new thread for each page when it becomeslarge
            threading.Thread(target=self.thread_function, args=(site,)).start()
        #     thrd =
        #         thrd
        #         thrds.append(thrd)
        # self.qu.join()
        # for t in thrds:
        #     t.join()
        # sithr.start()sithr =

    def runner_all(self):
        pass
