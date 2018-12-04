# -*- coding: utf-8 -*-

# ------ 精选菜谱 -----------

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
		douguo_container = response.css('div#container')
		douguo_cp_boxs = douguo_container.css('div.cp_box')
		for cp_box in douguo_cp_boxs:
			cp_box_href = cp_box.css('a::attr(href)').extract_first()
			yield Request(cp_box_href, RecipesParse().recipesDetail)


		next_page = response.css('div.pagination')
		if next_page == None:
			pass
		else:
			pagination_spans = next_page.css('span')
			pagination_spans.reverse()
			for span in pagination_spans:
				span_text = span.css('::text').extract_first()

				if span_text == u'下一页':
					span_a_href = span.css('a::attr(href)').extract_first()
					next_page_go = response.urljoin(span_a_href)
					yield Request(span_a_href, self.parse)
					break
