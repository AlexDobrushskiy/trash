#!/usr/bin/env python
# -*- coding: utf-8 -*-
from requests import get

def getpage(page):
	try:
		return get(page).text
	except:
		return ""

page = 'http://yandex.ru'
# page = 'Not "good" at all'
# <a href="http://yandex.ru">asdhgj</a>

# make a comment - Ctrl + /
def get_next_target(page):
	start_link = page.find('<a href=')
	if start_link == -1:
		return None, 0

	start_quote = page.find('"', start_link)
	end_quote = page.find('"', start_quote+1)
	url = page[start_quote+1:end_quote]
	return url, end_quote

# url, end = get_next_target(page)
# print url
# page1 = page[end:]
# url, end = get_next_target(page1)
# print url

def get_all_links(page):
	list_of_links = []
	while True: 
		url, endpos = get_next_target(page)
		if url:
			list_of_links.append (url)
			page = page[endpos:]
		else: 
			break 
	return list_of_links

def union(a, b):
	result = []
	for i in a+b:
		if i in result:
			pass
		else:
			result.append(i)
	
	return result


def crawl_web(seed, max_links):
	# список ссылок, которые нужно посетить
	to_crawl = [seed]
	# списиок уже посещенный ссылок
	crawled = []	
	# while to_crawl is not empty
	while to_crawl and len (crawled)<max_links: 
		page = to_crawl.pop()
		if page not in crawled:
			#proccess page
			to_crawl = union(to_crawl, get_all_links(getpage(page)))
			crawled.append(page)

	return crawled



links = crawl_web(page,3)

print links
#[<link1>, <link2>, ..]

