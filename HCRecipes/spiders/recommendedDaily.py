# ----- coding:utf-8 --------

# ---------- 每日推荐菜谱 -----------

import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from HCRecipes.recipesparse import RecipesParse
from HCRecipes.items import HcrecipesItem

class RecommendedDaily(scrapy.Spider):

	name = "RecommendedDaily"
	allowed_domains = ['www.douguo.com']
	bash_url = 'https://www.douguo.com'
	start_urls = ["https://www.douguo.com"]

	def parse(self,response):
		douguo_fContainers = response.css('div.fContainer')
		recipeparse = RecipesParse()
		isBrief = bool(getattr(self, 'isBrief', False))
		for fContainer in douguo_fContainers:
			retu_href = fContainer.css('p.retu a::attr(href)').extract_first()
			recipe = recipeparse.recipesDetail(retu_href)
			yield HcrecipesItem(recipe)

			
