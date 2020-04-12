from bs4 import BeautifulSoup
import unittest
import lxml


def parse(path_to_file):    
    # Поместите ваш код здесь.
    # ВАЖНО!!!
    # При открытии файла, добавьте в функцию open необязательный параметр
    # encoding='utf-8', его отсутствие в коде будет вызвать падение вашего
    # решения на грейдере с ошибкой UnicodeDecodeError
    with open(path_to_file, encoding='utf-8') as fil:
        html = fil.read()
        soup = BeautifulSoup(html, 'lxml')
        body = soup.find('div', id='bodyContent')

        imgs = get_images_amount(body)
        headers = get_headers_amount(body)
        linkslen = get_max_links_len(body)
        lists = get_lists_num(body)

    return [imgs, headers, linkslen, lists]

def get_images_amount(body):
    imgs = body.find_all('img')
    fit_imgs = len(
        [x for x in imgs if x.get('width') and int(x.get('width')) >= 200]
    )
    return fit_imgs

def get_headers_amount(body):
    headers_first = body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    headers_first = [header.text for header in headers_first]
    headers = []
    for i in range(len(headers_first)):
        if headers_first[i][0] in ['E','T','C']:
            headers.append(headers_first[i])

    return len(headers)

def get_max_links_len(body):
    all_links = body.find_all('a')
    linkslen = 0
    for link in all_links:
        current_count = 1
        siblings = link.find_next_siblings()
        for sibling in siblings:
            if sibling.name == 'a':
                current_count += 1
                linkslen = max(current_count, linkslen)
            else:
                current_count = 0
    return linkslen

def get_lists_num(body):
    all_lists = body.find_all(['ul', 'ol'])
    lists = 0
    for one_list in all_lists:
        if not one_list.find_parents(['ul','ol']):
            lists += 1
    return lists

