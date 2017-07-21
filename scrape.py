#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests

BASE_URL = 'https://gamesdonequick.com/'
DONATIONS_URL = 'tracker/donations'

def main():
	num_pages = get_num_pages()
	for page in range(1, num_pages):
		soup = get_soup(BASE_URL + DONATIONS_URL + '?page={}'.format(page))
		page_donations = get_donations_with_comments(soup)
		for donation in page_donations:
			donation_soup = get_soup(BASE_URL + donation)
			print(get_comment(donation_soup))

def get_donations_with_comments(soup):
	donation_urls = []

	table = soup.find('table')
	trs = table.find_all('tr')
	del trs[0] # Remove heading row

	for tr in trs:
		tds = tr.find_all('td')
		if tds[-1].string.strip() == 'Yes':
			a = tds[-2].find('a')
			donation_urls.append(a['href'])

	return donation_urls

def get_comment(soup):
	table = soup.find('table')
	trs = table.find_all('tr')
	td = trs[-1].find('td')
	return '\n'.join(td.stripped_strings)

def get_num_pages():
	soup = get_soup(BASE_URL + DONATIONS_URL)

	page_select = soup.find('select', attrs={'name': 'page'})
	page_options = page_select.find_all('option')
	return int(page_options[-1].string)

def get_soup(url):
	r = requests.get(url)
	r.encoding = 'utf-8'
	return BeautifulSoup(r.text, 'html.parser')


if __name__ == '__main__':
	main()
