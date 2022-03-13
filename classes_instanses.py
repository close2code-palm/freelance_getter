"""Project runner with scrape options and configuration of pre-defined objects"""

import threading

import argparse

from flsite import Site

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
habr_fl = Site(
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
threads_cnt_l = []
hfl_t = threading.Thread(target=show_parsed, args=(habr_fl, 'dev'))
threads_cnt_l.append(hfl_t)
# flru -bug with output + pro_only, don't need it
# flr_t = threading.Thread(target=show_parsed, args=(fl_ru, 'coding'))
# threads_cnt_l.append(flr_t)
fr_r_t = threading.Thread(target=show_parsed, args=(freenace_ru, 'python'))
threads_cnt_l.append(fr_r_t)

for t in threads_cnt_l:
    t.start()

for t in threads_cnt_l:
    t.join()
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
parser = argparse.ArgumentParser()

# Here builder pattern come into a play
parser.add_argument('-u',  '--update-db',
                    help='saves new results to the database', action='store_true')
parser.add_argument('spec', help='specialisations sites will be parsed for', type=str,
                    choices=['pydev', 'design', 'sysops'])

amount2get = parser.add_mutually_exclusive_group(required=True)
amount2get.add_argument('-f', '--fresh-only', help='shows only the last added propositions',
                        action='store_true')
parser.add_argument('-a', type=int, help='for how long you want to get information')
args = parser.parse_args()

