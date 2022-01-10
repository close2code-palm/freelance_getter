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
# print(habr_fl.job_suffixes)
# habr_fl.scrape('dev')
# habr_fl.show()
fl_ru.scrape('coding')
fl_ru.show()
# freenace_ru.scrape('python')
# freenace_ru.show()

# sites instation with all its data
# scanner intstation with sites
# scraper setting spec options, deep

# sites_fl_scanner = Scanner(1, habr_fl, freenace_ru, fl_ru)
# sites_fl_scanner.runner_h()
#
# habring_hot = threading.Thread(target=habr_fl.scrape_page())
# fling_hot = threading.Thread(target=fl_ru.scrape_page())
# freelancing_hot = threading.Thread(target=freenace_ru.scrape_page())
#
# def workout(th_name: threading.Thread):
#     th_name.start()
#     th_name.join()
#
# print(fl_ru)
# print(fling_hot)
# workout(fling_hot)
# workout(freelancing_hot)
#
# freenace_ru.show()
# print('\n----------------------------------'
#       '-------------------------------------------\n')


# workout(habring_hot)
# workout(fling_hot)
# workout(freelancing_hot)

#
# def show_all():
#     fl_ru.show()
#     freenace_ru.show()
#     habr_fl.show()
#
#
# ss = [fl_ru, habr_fl, freenace_ru]
# all_works = set()
# for site in ss:
#     all_works.add(threading.Thread(target=site.scrape()))
#
# for t in all_works:
#     workout(t)
#
# for s in ss:
#     s.show()
#
# fl_ru.scrape()
# fl_ru.show()
#
# habr_fl.scrape(2)

# habr_fl.show()

# show_all()
