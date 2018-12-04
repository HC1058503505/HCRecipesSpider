# -*- coding: utf-8 -*-

# ------- 菜谱的食材分类列表 --------
import sys
import requests
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from HCRecipes.items import HCFoodIngredients

reload(sys)
sys.setdefaultencoding('utf8')

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
			

			effect_url = self.base_url + '/ingredients/' + foopi_title + '/effect'
			xiangke_url = self.base_url + '/xiangke/' + foopi_title
			dapei_url = self.base_url + '/dapei/' + foopi_title
			
			effect_response = requests.get(effect_url)
			effect_response.encoding = 'utf-8'
			effect_bs = BeautifulSoup(effect_response.text, 'lxml')
			effect_bs_bkmcot = effect_bs.find_all('div', class_ = 'bkmcot')
			for bkmcot in effect_bs_bkmcot:
				bkmcot_h3 = bkmcot.find('h3', class_ = 'pbm')
				bkmcot_h3_id = bkmcot_h3.get('id')
				if bkmcot_h3_id == None:
					pass
				else:
					jieshao = ''
					chengfen = []
					if bkmcot_h3_id != 'chengfen':
						bkmcot_ps = bkmcot.find_all('p')
						for p in bkmcot_ps:
							p_text = p.get_text(strip=True)
							if len(p_text) == 0:
								continue
							jieshao = jieshao + p_text + '\n'
						jieshao.rstrip()
						print jieshao, bkmcot_h3_id
					elif bkmcot_h3_id == 'chengfen':
						bkmcot_table = bkmcot.find('table', class_='inrtab')
						bkmcot_table_trs = bkmcot_table.find_all('tr')
						for tr in bkmcot_table_trs:
							tr_text = tr.get_text('|',strip = True)
							tr_text_split = tr_text.split('|')
							if len(tr_text_split) == 4:
								chengfen_temp = [
										{
											'item_title' : tr_text_split[0],
											'item_value' : tr_text_split[1]
										},
										{
											'item_title' : tr_text_split[2],
											'item_value' : tr_text_split[3]
										}
									]

								chengfen = chengfen + chengfen_temp
							elif len(tr_text_split) == 2:
								chengfen.append({
										'item_title' : tr_text_split[0],
										'item_value' : tr_text_split[1]
									})
							else:
								pass

		# yield HCFoodIngredients({
		# 		'ingredients_title' : ingredients_title,
		# 		'ingredients_content' : ingredients_content
		# 	})


