# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HcrecipesItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	# 菜谱id
	recipe_id = scrapy.Field()
	# 菜谱标题
	recipe_title = scrapy.Field()
	# 菜谱介绍大图
	recipe_cover = scrapy.Field()
	# 菜谱浏览量
	recipe_views = scrapy.Field()
	# 菜谱收藏量
	recipe_collection = scrapy.Field()
	# 菜谱简介
	recipe_desc = scrapy.Field()
	# 菜谱难度以及材料
	recipe_materials = scrapy.Field()
	# 菜谱步骤
	recipe_steps = scrapy.Field()
	# 菜谱是否有视频
	recipe_hasvideo = scrapy.Field()
	# 菜谱视频url
	recipe_videosrc = scrapy.Field()
	# 菜谱分类标签
	reicpe_mortips = scrapy.Field()
	# 菜谱小贴士
	recipe_xtieshi = scrapy.Field()
class HCRecipeCalssification(scrapy.Item):
	
	# 分类标题
	classify_title = scrapy.Field()
	# 分类内容
	classify_content = scrapy.Field()
		


class HCFoodIngredients(scrapy.Item):
	
	# 分类标题
	ingredients_title = scrapy.Field()
	# 分类内容
	ingredients_sub_title = scrapy.Field()
	ingredients_img = scrapy.Field()
	ingredients_effect = scrapy.Field()
	ingredients_xiangke = scrapy.Field()
	ingredients_dapei = scrapy.Field()


class HCMenuRecipes(scrapy.Item):
	menu_id = scrapy.Field()
	menu_title = scrapy.Field()
	menu_scan_num = scrapy.Field()
	menu_collection_num = scrapy.Field()
	menu_desc = scrapy.Field()
	menu_sections = scrapy.Field()

		