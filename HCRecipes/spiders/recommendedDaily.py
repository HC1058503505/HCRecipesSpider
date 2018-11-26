# ----- coding:utf-8 --------

import re
import requests
import scrapy
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import Request
import time
import json

class RecommendedDaily(scrapy.Spider):

	name = "RecommendedDaily"
	allowed_domains = ['www.douguo.com']
	bash_url = 'https://www.douguo.com'
	start_urls = ["https://www.douguo.com"]

	def parse(self,response):
		douguo_bs = BeautifulSoup(response.text,'lxml') 
		douguo_hot_mb2 = douguo_bs.find('div', class_='hot')
	 	douguo_hot_mb2_div_cover = douguo_hot_mb2.find_all('div', class_='cover')
	 	for cover in douguo_hot_mb2_div_cover:
	 		cover_p_retu = cover.find('p', class_='retu')
	 		cover_p_retur_a = cover_p_retu.find('a')
	 		cover_p_retur_href = cover_p_retur_a['href']
	 		yield Request(cover_p_retur_href, self.recipesDetail)
	 		# break


	def recipesDetail(self, response):
		recipesDetail_bs = BeautifulSoup(response.text,'lxml')
		recipe_info = recipesDetail_bs.find('div', class_='recinfo')
		div_bokpic = recipe_info.find('div', class_='bokpic')
		div_bokpic_a = div_bokpic.find('a')
		div_bokpic_a_img = div_bokpic_a.find('img')
		# 图片
		div_bokpic_a_img_src = ['src']
		# 标题
		h1 = recipe_info.find('h1',id='page_cm_id')
		recipe_title = h1.text.strip()
		# 浏览搜藏
		falisc_div = recipe_info.find('div', class_='falisc')
		falisc_scan = falisc_div.find('span', class_='collectview')
		falisc_collection = falisc_div.find('span',class_='collectnum')
		# 材料
		retew_div = recipe_info.find('div',class_='retew')
		retew_div_table = retew_div.find('table',class_='retamr')
		retew_div_table_trs = retew_div_table.find_all('tr')
		

		zfliao_table = []
		zfliao_table_slices = self.sliceMtims(retew_div_table_trs)

		for slcie_trs in zfliao_table_slices:

			rows_list = []
			sections = []
			for i in range(len(slcie_trs)):
				tr = slcie_trs[i]
				if i == 0:
					section_title = tr.get_text('|', strip=True)
					sections = self.itemMtims(section_title)
				else:
					rows_text = tr.get_text('|', strip=True)
					rows = self.itemMtims(rows_text)
					rows_list = rows_list + rows

			section_dic = {'section_title' : sections, 'rows_list' : rows_list}
			zfliao_table.append(section_dic)

		# 做菜步骤
		recipes_steps = []
		retew_div_steps = retew_div.find('div',class_='step')

		retew_div_stepconts = retew_div_steps.find_all('div',class_='stepcont')

		
		for stepcont in retew_div_stepconts:

			stepcont_pldc = stepcont.find('div',class_='pldc')
			stepcont_pldc_a = stepcont_pldc.find('a')
			# 步骤图片href
			stepcont_pldc_a_href = stepcont_pldc_a['href']
			# 步骤文字介绍
			stepcont_pldc_p = stepcont.find('p')

			stepcont_pldc_p_text = stepcont_pldc_p.get_text(strip=True)
			recipes_steps.append({
					'step_img_href' : stepcont_pldc_a_href,
					'step_text' : stepcont_pldc_p_text
				})


			
		print '-------------------------------------------------------------'

	def sliceMtims(self,tbody_bs_tr):
		mtim = ()
		for tr in tbody_bs_tr:
			if tr.get("class") != None:
				tr_class = tr["class"]
				if 'mtim' in tr_class:
					index = tbody_bs_tr.index(tr)
					mtim = mtim + (index,)

		results = []		
		for i in range(len(mtim)):
			if i + 1 < len(mtim):
				slice_tr = tbody_bs_tr[mtim[i] : mtim[i + 1]]
			else:
				slice_tr = tbody_bs_tr[mtim[i] : ] 

			results.append(slice_tr)

		return results

	def itemMtims(self,item):
		params = item.split('|')
		params_count = len(params)
		if params_count == 1:
			return [{"item_title" : params[0], "item_value" : ""}]
		elif params_count == 2:
			return [{"item_title" : params[0], "item_value" : params[-1]}]
		elif params_count == 4:
			return [{"item_title" : params[0], "item_value" : params[1]},{"item_title" : params[2], "item_value" : params[3]}]










