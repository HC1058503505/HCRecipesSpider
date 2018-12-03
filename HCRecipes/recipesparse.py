# -*- coding: utf-8 -*-
import re
import urllib2
import time
import requests
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from HCRecipes.items import HcrecipesItem

class RecipesParse(object):

	def recipesDetail(self, response):
		# recipe id
		pattern = re.compile(r'https://www.douguo.com/cookbook/(.*?).html',)
		recipe_id = re.match(pattern,response.url).group(1)

		# recipe detail
		recipesDetail_bs = BeautifulSoup(response.text,'lxml')
		recipe_info = recipesDetail_bs.find('div', class_='recinfo')
		div_bokpic = recipe_info.find('div', class_='bokpic')
		div_bokpic_as = div_bokpic.find_all('a')

		hasvideo = False
		# 图片
		div_bokpic_a_img_src = ''
		div_video_a_href = ''
		if len(div_bokpic_as) == 0:
			pass
		elif len(div_bokpic_as) == 1:
			div_bokpic_a = div_bokpic_as[0]
			div_bokpic_a_img = div_bokpic_a.find('img')
			div_bokpic_a_img_src = div_bokpic_a_img['src']
		elif len(div_bokpic_as) == 2:
			div_bokpic_a = div_bokpic_as[0]
			div_bokpic_a_img = div_bokpic_a.find('img')
			div_bokpic_a_img_src = div_bokpic_a_img['src']

			hasvideo = True
			div_video_a = div_bokpic_as[1]
			div_video_a_href = div_video_a['href']
			
		
		# 标题
		h1 = recipe_info.find('h1',id='page_cm_id')
		recipe_title = h1.text.strip()
		# 浏览搜藏
		falisc_div = recipe_info.find('div', class_='falisc')
		falisc_scan = falisc_div.find('span', class_='collectview').text
		falisc_collection = falisc_div.find('span',class_='collectnum').text
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
					# section_title = tr.get_text('|', strip=True)
					# sections = self.itemMtims(section_title)
					sections = self.parseTr(tr)
				else:
					# rows_text = tr.get_text('|', strip=True)
					# rows = self.itemMtims(rows_text)
					rows = self.parseTr(tr)
					if rows == None:
						print rows_text
						print recipe_title
					rows_list = rows_list + rows

			section_dic = {'section_title' : sections, 'rows_list' : rows_list}
			zfliao_table.append(section_dic)

		# 做菜步骤
		recipes_steps = []
		retew_div_steps = retew_div.find('div',class_='step')

		retew_div_stepconts = retew_div_steps.find_all('div',class_='stepcont')
		if retew_div_stepconts == None or len(retew_div_stepconts) == 0:
			pass
		else: 
			for stepcont in retew_div_stepconts:

				stepcont_pldc = stepcont.find('div',class_='pldc')
				if stepcont_pldc == None:
					stepcont_p = stepcont.find('p')
					stepcont_p_text = stepcont_p.get_text(strip=True)
					recipes_steps.append({
							'step_img_href' : '',
							'step_text' : stepcont_p_text
						})
				else:
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

		# 分类
		reicpe_mortips = []
		retew_div_mortips = retew_div.find('div',class_='mortips')
		if retew_div_mortips == None:
			pass
		else:
			retew_div_mortips_spans = retew_div_mortips.find_all('span')
			for span in retew_div_mortips_spans:
				span_a = span.find('a')
				span_a_text = span_a.get_text(strip=True)
				reicpe_mortips.append(span_a_text)

		# 菜谱Item
		recipe_model = HcrecipesItem({
					'recipe_id' : recipe_id,
					'recipe_title' : recipe_title,
					'recipe_cover' : div_bokpic_a_img_src,
					'recipe_views' : falisc_scan,
					'recipe_collection' : falisc_collection,
					'recipe_materials' : zfliao_table,
					'recipe_steps' : recipes_steps,
					'recipe_hasvideo' : hasvideo, 
					'recipe_videosrc' : '',
					'reicpe_mortips' : reicpe_mortips
				})
		
		if hasvideo:
			yield Request(div_video_a_href, self.parseVideo, meta=recipe_model)
		else:
			yield recipe_model

	def parseVideo(self, response):
		video_html_bs = BeautifulSoup(response.text, 'lxml')
		video_html_bs_embed = video_html_bs.find('embed')
		video_src = video_html_bs_embed['src']
		recipesItem = response.meta
		recipesItem['recipe_videosrc'] = video_src
		yield recipesItem

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

	def parseTr(self,tr):
		tds = tr.find_all('td')
		td_left = tds[0]
		td_right = tds[-1]
		sections = []
		for td in tds:
			td_text = td.get_text('|', strip=True)
			td_text_split = td_text.split('|')
			item_title = ""
			item_value = ""

			if len(td_text_split) == 0:
				pass
			elif len(td_text_split) == 1:
				item_title = td_text_split[0]
			elif len(td_text_split) == 2:
				item_title = td_text_split[0]
				item_value = td_text_split[1]

			sections.append({
					"item_title" : item_title,
					"item_value" : item_value
				})

		return sections