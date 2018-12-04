# ----- coding:utf-8 --------

# ---------- 每日推荐菜谱 -----------

import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from HCRecipes.recipesparse import RecipesParse

class RecommendedDaily(scrapy.Spider):

	name = "RecommendedDaily"
	allowed_domains = ['www.douguo.com']
	bash_url = 'https://www.douguo.com'
	start_urls = ["https://www.douguo.com"]

	def parse(self,response):
		douguo_fContainers = response.css('div.fContainer')
		for fContainer in douguo_fContainers:
			retu_href = fContainer.css('p.retu a::attr(href)').extract_first()
			yield Request(retu_href, RecipesParse().recipesDetail)

