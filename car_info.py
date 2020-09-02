#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import sys
import json


def get_html(url):
	r = requests.get(url)
	r.encoding = 'utf-8'
	return r

def printer(dictionary):
	for k, v in dictionary.items():
		print(k, ':', v)

def get_car_attr(soup):
	attr = str(soup.find('div', id = 'sale-data-attributes'))
	attr = attr.replace('<div data-bem=\'{\"sale-data-attributes\":', '')
	end = attr.find('}}')
	attr = attr[:end + 1]
	dictionary = json.loads(attr)
	car_attr = {'mark' : dictionary['markName'],
				'model' : dictionary['modelName'],
				'engine_type' : dictionary['engine-type'],
				'km_age' : dictionary['km-age'],
				'power' : dictionary['power'],
				'price' : dictionary['price'],
				'gearbox' : dictionary['transmission'],
				'year' : dictionary['year']
				}
	return car_attr

def get_card_info(soup):
	card_info = {}
	for tag in soup.find_all('span', class_ = 'CardInfo__cell'):
		if tag.text == 'Кузов':
			card_info['body_type'] = tag.find_next('span').get_text()
		if tag.text == 'Двигатель':
			engine = tag.find_next('span').get_text()
			card_info['displacement'] = float(engine[:engine.find(' л')])
		if tag.text == 'Привод':
			card_info['gear_type'] = tag.find_next('span').get_text()
		if tag.text == 'Руль':
			card_info['steering_wheel'] = tag.find_next('span').get_text()
		if tag.text == 'Владельцы':
			card_info['owners_number'] = int(tag.find_next('span').get_text()[:1])
	return card_info

def get_owner_info(soup):
	try:
		private = soup.find('div', class_ = 'CardSellerNamePlace__name').get_text()
		private_person = True
	except:
		private_person = False 

	city = soup.find('span', class_ = 'MetroListPlace__regionName').get_text()
	owner_info = {'private_person' : private_person,
					'city' : city
				}
	return owner_info

def get_generation(soup):
	cat_link = soup.find('a', class_ = 'CardCatalogLink').get('href')
	html = get_html(cat_link)
	cat_soup = BeautifulSoup(html.text, 'lxml')
	gen_name = cat_soup.find('a', class_ = 'search-form-v2-mmm__breadcrumbs-item_type_generation').get_text()
	generation = {'generation' : gen_name}
	return generation

def get_content(html):
	soup = BeautifulSoup(html, 'lxml')
	car_attr = get_car_attr(soup)
	card_info = get_card_info(soup)
	car_gen = get_generation(soup)
	owner_info = get_owner_info(soup)
	car_attr.update(card_info)
	car_attr.update(car_gen)
	car_attr.update(owner_info)
	printer(car_attr)
	
def parse(url):
	html = get_html(url)
	get_content(html.text)

def main():
	if len(sys.argv) == 1:
		print('The program does not have a link to data')
		sys.exit()
	else:
		link = sys.argv[1]
	parse(link)

if __name__ == '__main__':
	main()
