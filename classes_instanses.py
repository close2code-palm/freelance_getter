import _thread
import threading

from flsite import Site

fl_ru = Site(
    'https://www.fl.ru',
    'FL.RU',
    6,
    ['/projects/category/programmirovanie', '/?page='],
    ('a', {'class': 'b-post__link'}), ('div', {'class': 'b-post__price'}),
    ('div', {'class': 'b-post__txt'})
)

freenace_ru = Site(
    'https://freelance.ru',
    'FREELANCE.RU',
    6,
    ['/project/search/pro?c=&q=python&m=or&e=&f=&t=&o=0&o=1', '&page='],
    ('a', {'title': 'Название'}), ('div', {'class': 'cost'}), ('time', {'class': 'timeago'})
)

habr_fl_1f = 'div', {"class": "task__title"}
habr_fl_2f = 'span', {'class': 'count'}
habr_fl_3f = 'span', {"class": "params__published-at"}
habr_fl = Site(
    'https://freelance.habr.com',
    'HABRFL',
    10,
    ['/tasks', '?page='],
    habr_fl_1f, habr_fl_2f, habr_fl_3f
)

# habring_hot = threading.Thread(target=habr_fl.scrape_page())
fling_hot = threading.Thread(target=fl_ru.scrape_page())
freelancing_hot = threading.Thread(target=freenace_ru.scrape_page())

def workout(th_name: threading.Thread):
    th_name.start()
    th_name.join()

print(fl_ru)
print(fling_hot)
workout(fling_hot)
workout(freelancing_hot)

freenace_ru.show()
print('\n----------------------------------'
      '-------------------------------------------\n')


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

habr_fl.scrape()
habr_fl.show()

# show_all()
