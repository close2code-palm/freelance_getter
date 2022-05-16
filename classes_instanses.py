"""Project runner with scrape options and configuration of pre-defined objects"""
import os
import sys
import threading
import time

import argparse
from playsound import playsound
from win32ctypes.pywin32 import win32api

from alerting import notify_w_job
from flsite import Site, HabrFlSite

# fl_ru = Site(
#     'https://www.fl.ru',
#     'FL.RU',
#     6,
#     {'coding': '/projects/category/programmirovanie',
#      'sites': '/projects/category/razrabotka-sajtov',
#      '3D': '/projects/category/3d-grafika/',
#      'pager': '/?page='},
#     ('a', {'class': 'b-post__link'}), ('div', {'class': 'b-post__price'}),
#     ('div', {'class': 'b-post__txt'}),
#     js=True
# )

# TODO make a yaml config for user, factory for instansiating

freenace_ru = Site(
    'https://freelance.ru',
    'FREELANCE.RU',
    6,
    {'python': '/project/search/pro?c=&q=python&m=or&e=&f=&t=&o=0&o=1',
     'parsing': '/project/search/pro?c=&q=парс&m=or&e=&f=&t=&o=0&o=1',
     'design/photo': '/project/search/pro?c=&c[]=40&c[]=577&c[]=98&q=&m=or&e=&f=&t=&o=0&o=1',
     'pager': '&page='},
    ('a', {'title': 'Название'}), ('div', {'class': 'cost'}), ('time', {'class': 'timeago'}),
)

habr_fl_1f = 'div', {"class": "task__title"}
habr_fl_2f = 'span', {'class': 'count'}
habr_fl_3f = 'span', {"class": "params__published-at"}
habr_fl_4f = 'div.task__tittle a[href]'
# habr_fl = Site(
#     'https://freelance.habr.com',
#     'HABRFL',
#     10,
#     {'all': '/tasks',
#      'dev': '/tasks?categories=development_all_inclusive,development_backend\
#      ,development_frontend,development_prototyping,development_ios,development_android,\
#      development_desktop,development_bots,development_games,development_1c_dev,development_scripts,\
#      development_voice_interfaces,development_other',
#      'testing': '/tasks?categories=testing_sites,testing_mobile,testing_software',
#      'design': '/tasks?categories=design_sites,design_landings,design_logos,design_illustrations,\
#      design_mobile,design_icons,design_polygraphy,design_banners,design_graphics,design_corporate_identity,\
#      design_presentations,design_modeling,design_animation,design_photo,design_other',
#      'pager': '?page='},
#     habr_fl_1f, habr_fl_2f, habr_fl_3f,
# )

explicit_habr = HabrFlSite(
    'https://freelance.habr.com',
    'HABRFL',
    10,
    {'all': '/tasks',
     'dev': '/tasks?categories=development_all_inclusive,development_backend\
     ,development_frontend,development_prototyping,development_ios,development_android,\
     development_desktop,development_bots,development_games,development_1c_dev,development_scripts,\
     development_voice_interfaces,development_other',
     'testing': '/tasks?categories=testing_sites,testing_mobile,testing_software',
     'design': '/tasks?categories=design_sites,design_landings,design_logos,design_illustrations,\
     design_mobile,design_icons,design_polygraphy,design_banners,design_graphics,design_corporate_identity,\
     design_presentations,design_modeling,design_animation,design_photo,design_other',
     'pager': '?page='},
    habr_fl_4f,
    habr_fl_1f, habr_fl_2f, habr_fl_3f,
)


# upwrk = Site('https://www.upwork.com/freelance-jobs/python-script/',
#              'UPWORK', )


def show_parsed(flst: Site, *keys):
    flst.scrape(*keys)
    flst.show()


# _thread.start_new_thread(show_parsed, (habr_fl, 'dev'))
# _thread.start_new_thread(show_parsed, (fl_ru, 'coding'))
# _thread.start_new_thread(show_parsed, (freenace_ru, 'python'))
# flru -bug with output + pro_only, don't need it
# flr_t = threading.Thread(target=show_parsed, args=(fl_ru, 'coding'))
# threads_cnt_l.append(flr_t)
threads_cnt_l = []
fr_r_t = threading.Thread(target=show_parsed, args=(freenace_ru, 'python'))
threads_cnt_l.append(fr_r_t)


#
# connectn = psycopg2.connect(user='postgres',
#                             password='wont4Org!0',
#                             host='localhost',
#                             port='5433',
#                             database='working_data')
#
# res_fr_habrfl = habr_fl.job_headers
# print(res_fr_habrfl[0].id)
#
# try:
#     cursr = connectn.cursor()
#
#
#     def build_query_n_exct(headers: [WorkHeaders]):
#
#         query = f'''INSERT INTO fl_offers (uid, reward, full_dscrptn, timings)
#          VALUES (%s,%s,%s,%s);'''
#
#         for header in headers:
#             cursr.execute(query, (header.id, header.price, header.descr, header.util_info))
#         connectn.commit()
#
#
#     build_query_n_exct(habr_fl.job_headers)
#     build_query_n_exct(freenace_ru.job_headers)
#
# finally:
#     if connectn:
#         cursr.close()
#         connectn.close()
def parser_constructor():
    """initialize the argparser"""
    prg_dscr = 'All in one for job offers and proposal data processing'
    prg_name = 'Jobipy'
    usg = 'Use this just if you aren\'t afraid of burning out'
    arg_parser = argparse.ArgumentParser(prog=prg_name, usage=usg, description=prg_dscr)
    return arg_parser


parser = parser_constructor()
# Here builder pattern come into a play
# parser.add_argument('-u',  '--update-db',
#                     help='saves new results to the database', action='store_true')
parser.add_argument('spec', help='specialisations sites will be parsed for', type=str,
                    choices=['pydev', 'design', 'sysops', 'preconfigured'])
parser.add_argument('-n', '--notify', help='parses within loop and sends notifications',
                    action='store_true', default=False)

amount2get = parser.add_mutually_exclusive_group(required=True)
amount2get.add_argument('-f', '--fresh-only', help='shows only the last added propositions',
                        action='store_true')
amount2get.add_argument('-a', type=int, help='for how long you want to get information',
                        action='store',
                        default=1,
                        nargs='?')
prsd_args = parser.parse_args()


# print(prsd_args)
# print(prsd_args.a)
# print(prsd_args.fresh_only)
# print(prsd_args.spec)
# hfl_t = threading.Thread(target=show_parsed, args=(habr_fl,
#                                                    'all', prsd_args.a))
# threads_cnt_l.append(hfl_t)
# if prsd_args.spec == 'preconfigured':
#     for t in threads_cnt_l:
#         t.start()
#
#     for t in threads_cnt_l:
#         t.join()

# todo add delta_storage to flsite.scraped

def notify_loop(theme, needed_tags):
    needed_tags = ['python', 'парс', 'bot', 'django', 'pars', 'бот']

    def _check_tags(tag, job_container):
        for fl_tag in job_container.tags:
            if tag in fl_tag:
                return True

    while True:
        loop_timeout = 150
        explicit_habr.scrape(theme=theme)
        if explicit_habr.last_scan:
            for job_article in explicit_habr.last_scan:
                for tag in needed_tags:
                    if tag in job_article.descr or _check_tags(tag, job_article):
                        notify_w_job(job_article)
                        loop_timeout -= 5
                        break
        if loop_timeout > 0:
            time.sleep(loop_timeout)


# todo add termination mechanism

if prsd_args.notify:
    fl_waiter = threading.Thread(target=notify_loop,
                                 args=('all', ['python', 'парс', 'bot', 'django', 'pars', 'бот'],))
    fl_waiter.start()
    try:
        fl_waiter.join()
    except KeyboardInterrupt:
        sys.exit(1)
