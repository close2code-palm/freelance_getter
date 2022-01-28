import _thread
import threading

from flsite import Site
from threader import Scanner

fl_ru = Site(
    'https://www.fl.ru',
    'FL.RU',
    6,
    {'coding': '/projects/category/programmirovanie',
     'sites': '/projects/category/razrabotka-sajtov',
     '3D': '/projects/category/3d-grafika/',
     'pager': '/?page='},
    ('a', {'class': 'b-post__link'}), ('div', {'class': 'b-post__price'}),
    ('div', {'class': 'b-post__txt'}),
    js=True
)

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


def show_parsed(flst: Site, *keys):
    flst.scrape(*keys)
    flst.show()


# _thread.start_new_thread(show_parsed, (habr_fl, 'dev'))
# _thread.start_new_thread(show_parsed, (fl_ru, 'coding'))
# _thread.start_new_thread(show_parsed, (freenace_ru, 'python'))
threads_cnt_l = []
hfl_t = threading.Thread(target=show_parsed, args=(habr_fl, 'dev'))
threads_cnt_l.append(hfl_t)
flr_t = threading.Thread(target=show_parsed, args=(fl_ru, 'coding'))
threads_cnt_l.append(flr_t)
fr_r_t = threading.Thread(target=show_parsed, args=(freenace_ru, 'python'))
threads_cnt_l.append(fr_r_t)

for t in threads_cnt_l:
    t.start()

for t in threads_cnt_l:
    t.join()
