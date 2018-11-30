# -*- coding: utf-8 -*-


import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from HCRecipes.items import HCFoodIngredients

class FoodIngredients(scrapy.Spider):
	name = "FoodIngredients"
	allowed_domains = ['www.douguo.com']
	base_url = 'https://www.douguo.com'
	start_urls = ["https://www.douguo.com/shicai/"]

	def parse(self, response):
		food_ingredients_bs = BeautifulSoup(response.text, 'lxml')
		food_ingredients_main = food_ingredients_bs.find('div', id = 'main')
		food_ingredients_caicont = food_ingredients_main.find('div', class_ = 'caicont')
		food_ingredients_caicontl = food_ingredients_caicont.find_all('div', class_ = 'caicontl')
		for caicontl in food_ingredients_caicontl:
			caicontl_a = caicontl.find('a')
			caicontl_a_href = caicontl_a['href']
			caicontl_url = self.base_url + caicontl_a_href
			yield Request(caicontl_url, self.ingredientsDetail)

	def ingredientsDetail(self, response):
		ingredients_detail_bs = BeautifulSoup(response.text, 'lxml')
		ingredients_detail_main = ingredients_detail_bs.find('div', id = 'main')
		ingredients_detail_caicont = ingredients_detail_main.find('div', class_ = 'caicont')
		ingredients_detail_caicontl = ingredients_detail_caicont.find('div', class_ = 'caicontl')
		ingredients_detail_caicontr = ingredients_detail_caicont.find('div', class_ = 'caicontr')
		ingredients_detail_caicontr_foopi = ingredients_detail_caicontr.find_all('div', class_ = 'foopi')
		ingredients_title = ingredients_detail_caicontl.get_text(strip = True)
		ingredients_content = []
		for foopi in ingredients_detail_caicontr_foopi:
			foopi_title = foopi.get_text(strip = True)
			foopi_img = foopi.find('img')
			foopi_img_src = foopi_img['src']
			ingredients_content.append({
					'ingredients_sub_title' : foopi_title,
					'ingredients_img' : foopi_img_src
				})
			

		yield HCFoodIngredients({
				'ingredients_title' : ingredients_title,
				'ingredients_content' : ingredients_content
			})


