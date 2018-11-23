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
	 		break

	def recipesDetail(self, response):
		recipesDetail_bs = BeautifulSoup(response.text,'lxml')
		div_bokpic = recipesDetail_bs.find('div', class_='bokpic')
		div_bokpic_a = div_bokpic.find('a')
		div_bokpic_a_img = div_bokpic_a.find('img')
		print div_bokpic_a_img['href']
		