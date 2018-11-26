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
		print len(zfliao_table_slices)
		for slcie in zfliao_table_slices:
			pass


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













