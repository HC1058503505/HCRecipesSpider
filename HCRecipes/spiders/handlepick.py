# -*- coding: utf-8 -*-


import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from HCRecipes.recipesparse import RecipesParse

class HandlePick(scrapy.Spider):
	
	name = "HandlePick"
	allowed_domains = ['www.douguo.com']
	bash_url = 'https://www.douguo.com'
	start_urls = [u"https://www.douguo.com/caipu/"]
	
	def parse(self, response):
		douguo_bs = BeautifulSoup(response.text,'lxml')
		douguo_bs_div_main = douguo_bs.find('div',id='main')
		douguo_bs_pagediv = douguo_bs_div_main.find('div', class_='pagediv')
		douguo_bs_pagediv_pagination = douguo_bs_pagediv.find('div', class_='pagination')
		douguo_bs_pagediv_spans = douguo_bs_pagediv_pagination.find_all('span')
		spans_text = map(self.spantext, douguo_bs_pagediv_spans)
		maxPage = max(spans_text)

		for i in range(maxPage):
			url = response.url + str(i * 30)
			print url
			yield Request(url, self.allPages)
				

	def allPages(self, response):
		douguo_bs = BeautifulSoup(response.text,'lxml')
		douguo_bs_div_main = douguo_bs.find('div',id='main')
		douguo_main_div_container = douguo_bs_div_main.find('div', id='container')
		douguo_container_cp_box = douguo_main_div_container.find_all('div', class_='cp_box')
		for cp_box in douguo_container_cp_box:
			cp_box_a = cp_box.find('a')
			if cp_box_a['href'] != None:
				cp_box_a_href = cp_box_a['href']
				yield Request(cp_box_a_href, RecipesParse().recipesDetail)
		
	def spantext(self, span):
		page = 0
		span_a = span.a
		if span_a == None:
			span_text = span.get_text(strip=True)
			page = int(span_text)
		else:
			span_a_href = span_a['href']
			span_a_href_split = span_a_href.split('/')
			page = int(span_a_href_split[-1]) / 30 + 1
		
		return page
