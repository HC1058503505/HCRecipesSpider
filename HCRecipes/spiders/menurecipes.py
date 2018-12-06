# ----- coding:utf-8 --------

# ---------- 菜单 -----------

import re
import requests
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from HCRecipes.items import HCMenuRecipes


class MenuRecipes(scrapy.Spider):

	name = "MenuRecipes"
	allowed_domains = ['www.douguo.com']
	bash_url = 'https://www.douguo.com'
	start_urls = ["https://www.douguo.com/caipu/caidan"]

	def parse(self, response):
		menu_bs = BeautifulSoup(response.text, 'lxml')
		menu_moards = menu_bs.find_all('div', class_ = 'moard')
		for moard in menu_moards:
			moard_h3 = moard.find('h3')
			moard_h3_text = moard_h3.get_text(strip = True)
			moard_h3_a = moard_h3.find('a')
			moard_h3_a_href = moard_h3_a['href']
			yield Request(moard_h3_a_href, self.menulist)

		# 下一页
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
					yield Request(next_page_go, self.parse)
					break


	def menulist(self, response):
		# recipe id
		# https://www.douguo.com/caipu/caidan/7822584.html
		pattern = re.compile(r'https://www.douguo.com/caipu/caidan/(.*?).html',)
		menu_id = re.match(pattern,response.url).group(1)
		menu_bs = BeautifulSoup(response.text, 'lxml')
		menu_meview = menu_bs.find('div', class_ = 'meview')
		menu_meview_melef = menu_meview.find('div', class_ = 'melef')
		menu_meview_h1 = menu_meview_melef.find('h1')
		menu_tilte = menu_meview_h1.get_text(strip = True)
		menu_meview_melef_spans = menu_meview_melef.find_all('span')

		# 浏览量，收藏量
		scan_num = 0
		collection_num = 0
		if len(menu_meview_melef_spans) == 4:
			scan_num_span = menu_meview_melef_spans[2]
			collection_num_span = menu_meview_melef_spans[3]

			scan_num_text = scan_num_span.get_text(strip = True)
			collection_num_text = collection_num_span.get_text(strip = True)

			pattern = re.compile('\d+')
			scan_num = int(pattern.findall(scan_num_text)[0])
			collection_num = int(pattern.findall(collection_num_text)[0])


		# 菜单简介
		menu_meview_mjie = menu_meview.find('div', class_ = 'mjie')
		menu_desc = menu_meview_mjie.get_text('\n', strip = True)
		menu_desc = menu_desc.strip()

		# 菜单列表
		menu_mecai = menu_bs.find('div', class_ = 'mecai')
		menu_mecai_left = menu_mecai.find_all('div', class_ = 'left')

		keone_pattern = re.compile(r'https://www.douguo.com/cookbook/(.*?).html',)
		
		menu_sections = []
		for left in menu_mecai_left:
			
			section_title = ''
			left_mtih2 = left.find('h2', class_ = 'mtih2')
			if left_mtih2 == None:
				pass
			else:
				section_title = left_mtih2.get_text(strip = True)

			left_keone = left.find_all('div', class_ = 'keone')
			recipe_list = []
			for keone in left_keone:
				keone_a = keone.find('a')
				keone_a_href = keone_a["href"]
				recipe = self.recipeBrief(keone_a_href)
				recipe_list.append(recipe)

			menu_sections.append({
					"section_title" : section_title,
					"recipe_list" : recipe_list
				})

		yield HCMenuRecipes({
				"menu_id" : menu_id,
				"menu_title" : menu_tilte,
				"menu_scan_num" : scan_num,
				"menu_collection_num" : collection_num,
				"menu_desc" : menu_desc,
				"menu_sections" : menu_sections
			})

	def recipeBrief(self,url):
		response = requests.get(url)
		response.encoding = 'utf-8'

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

		retew_div = recipe_info.find('div',class_='retew')

		return {
			"recipe_id" : recipe_id,
			"recipe_title" : recipe_title,
			'recipe_cover' : div_bokpic_a_img_src,
			'recipe_views' : falisc_scan,
			'recipe_collection' : falisc_collection,
			"recipe_hasvideo" : hasvideo
		}

















