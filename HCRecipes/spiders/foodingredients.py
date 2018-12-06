# -*- coding: utf-8 -*-

# ------- 菜谱的食材分类列表 --------
import re
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

		for foopi in ingredients_detail_caicontr_foopi:
			foopi_title = foopi.get_text(strip = True)
			foopi_img = foopi.find('img')
			foopi_img_src = foopi_img['src']

			# 营养成分
			effect_url = self.base_url + '/ingredients/' + foopi_title + '/effect'
			effect_components = self.shicaiEffectComponents(effect_url)

			# 食物相克
			xiangke_url = self.base_url + '/xiangke/' + foopi_title
			xiangke_components = self.shicaiXiangkeDapeiComponents(xiangke_url)
			
			# 食材搭配
			dapei_url = self.base_url + '/dapei/' + foopi_title
			dapei_componets = self.shicaiXiangkeDapeiComponents(dapei_url)


			yield HCFoodIngredients({
					'ingredients_title' : ingredients_title,
					'ingredients_sub_title' : foopi_title,
					'ingredients_img' : foopi_img_src,
					'ingredients_effect' : effect_components,
					'ingredients_xiangke' : xiangke_components,
					'ingredients_dapei' : dapei_componets
				})

	def shicaiEffectComponents(self, effect_url):
		effect_response = requests.get(effect_url)
		effect_response.encoding = 'utf-8'
		effect_bs = BeautifulSoup(effect_response.text.replace('<br />','\n'), 'lxml')
		effect_bs_bkmcot = effect_bs.find_all('div', class_ = 'bkmcot')
		effect_components = []
		for bkmcot in effect_bs_bkmcot:
			effectcomponent = None
			bkmcot_h3 = bkmcot.find('h3', class_ = 'pbm')
			bkmcot_h3_text = bkmcot_h3.get_text(strip = True)
			bkmcot_h3_id = bkmcot_h3.get('id')

			bkmcot_ps = bkmcot.find_all('p')
			if len(bkmcot_ps) == 0:
				chengfen = []
				bkmcot_table = bkmcot.find('table', class_='inrtab')
				if bkmcot_table == None:
					pass
				else:
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
				effectcomponent = {
					"effectcom_title" : bkmcot_h3_text,
					"effectcom_id" : bkmcot_h3_id,
					"effectcom_chengfen" : chengfen
				}
			else:
				componet_text = ''
				for p in bkmcot_ps:
					p_text = p.get_text(strip=True)
					if len(p_text) == 0:
						continue
					componet_text = componet_text + p_text + '\n'
					componet_text.rstrip()

				effectcomponent = {
					"effectcom_title" : bkmcot_h3_text,
					"effectcom_id" : bkmcot_h3_id,
					"effectcom_content" : componet_text
				}

			effect_components.append(effectcomponent)

		return effect_components


	def shicaiXiangkeDapeiComponents(self, xiangke_dapei_url):
		xiangke_dapei_response = requests.get(xiangke_dapei_url)
		xiangke_dapei_response.encoding = 'utf-8'
		xiangke_dapei_bs = BeautifulSoup(xiangke_dapei_response.text, 'lxml')
		xiangke_dapei_shicnr = xiangke_dapei_bs.find('div', class_='shicnr')
		xiangke_dapei_shicnr_h1 = xiangke_dapei_shicnr.find('h1', class_ = 'shez')
		xiangke_dapei_shicnr_desc_title = xiangke_dapei_shicnr_h1.get_text(strip = True)
		xiangke_dapei_shicnr_p = xiangke_dapei_shicnr.find('p', class_ = 'cdnr')
		xiangke_dapei_shicnr_desc = xiangke_dapei_shicnr_p.get_text(strip = True)


		xiangke_dapei_scsj_rs = xiangke_dapei_bs.find_all('div', class_ = 'scsj_r')
		xiangke_dapei_components = []
		for scsj_r in xiangke_dapei_scsj_rs:
			scsj_r_content = scsj_r.get_text(strip = True)
			scsj_r_content = scsj_r_content.replace('查看菜谱>>','')
			xiangke_dapei_components.append(scsj_r_content)
		return {
			"xiangke_dapei_title" : xiangke_dapei_shicnr_desc_title,
			"xiangke_dapei_desc" : xiangke_dapei_shicnr_desc,
			"xiangke_dapei_details" : xiangke_dapei_components
		}
