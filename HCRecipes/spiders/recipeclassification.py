# -*- coding: utf-8 -*-

# ------ 菜谱的分类列表 ------

import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from HCRecipes.items import HCRecipeCalssification

class RecipeCalssification(scrapy.Spider):
	name = "RecipesCalssification"
	allowed_domains = ['www.douguo.com']
	bash_url = 'https://www.douguo.com'
	start_urls = ["https://www.douguo.com/caipu/fenlei/"]

	def parse(self, response):
		recipe_classification_bs = BeautifulSoup(response.text, 'lxml')
		recipe_classification_main = recipe_classification_bs.find('div', id='main')
		recipe_classification_sortf = recipe_classification_main.find('div', class_='sortf')
		recipe_classification_subs = recipe_classification_sortf.find_all('div',class_=['fei3', 'libdm', 'pbl'])


		for sub in recipe_classification_subs:
			classification_sub_h2 = sub.find('h2')
			classification_sub_title = classification_sub_h2.get_text(strip=True)
			classification_sub_ul = sub.find('ul',class_='kbi')
			classification_sub_ul_lis = classification_sub_ul.find_all('li')
			classification_sub_ul_lis_text = classification_sub_ul.get_text('|',strip=True)
			classification_subs = classification_sub_ul_lis_text.split('|')

			yield HCRecipeCalssification({
					'classify_title' : classification_sub_title,
					'classify_content' : classification_subs
				})
		