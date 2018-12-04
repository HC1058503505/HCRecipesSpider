# ----- coding:utf-8 --------

# ------- 按类别分类的菜谱 --------

import sys
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from HCRecipes.recipesparse import RecipesParse

reload(sys)
sys.setdefaultencoding('utf8')

class RecipesFromClassify(scrapy.Spider):
	name = "RecipesFromClassify"
	allowed_domains = ['www.douguo.com']
	base_url = 'https://www.douguo.com'

	calssifies = [
					{"classify_content": ["\u5ddd\u83dc", "\u6e58\u83dc", "\u7ca4\u83dc", "\u9c81\u83dc", "\u4e1c\u5317\u83dc", "\u897f\u5317\u83dc", "\u6d59\u83dc", "\u82cf\u83dc", "\u4e0a\u6d77\u83dc", "\u4eac\u83dc", "\u95fd\u83dc", "\u5fbd\u83dc", "\u664b\u83dc", "\u6dee\u626c\u83dc", "\u6e05\u771f", "\u5ba2\u5bb6\u83dc", "\u65b0\u7586\u83dc", "\u8d35\u5dde\u83dc", "\u8c6b\u83dc", "\u4e91\u5357\u83dc", "\u9102\u83dc", "\u8d63\u83dc", "\u53f0\u6e7e\u7f8e\u98df", "\u9999\u6e2f\u7f8e\u98df", "\u6fb3\u95e8\u7f8e\u98df", "\u897f\u9910", "\u6cd5\u56fd\u83dc", "\u610f\u5927\u5229\u83dc", "\u65e5\u672c\u6599\u7406", "\u97e9\u56fd\u6599\u7406", "\u6cf0\u56fd\u83dc", "\u4e1c\u5357\u4e9a\u7f8e\u98df", "\u5bb6\u5e38\u83dc", "\u5929\u6d25\u83dc"], "classify_title": "\u83dc\u7cfb"},
					{"classify_content": ["\u714e", "\u7092", "\u70b8", "\u7ea2\u70e7", "\u716e", "\u84b8", "\u70e7\u70e4", "\u7116", "\u7096", "\u62cc", "\u70d9", "\u814c", "\u7117", "\u5364", "\u69a8\u6c41", "\u70e4", "\u70e9", "\u7172", "\u514d\u70e4", "\u5e72\u7178", "\u718f", "\u9171", "\u7802\u9505", "\u5e72\u9505", "\u7168", "\u712f", "\u6dae", "\u5176\u4ed6\u5de5\u827a"], "classify_title": "\u70f9\u996a\u65b9\u6cd5"},
					{"classify_content": ["\u9178", "\u751c", "\u8fa3", "\u54b8", "\u9999", "\u82e6", "\u9c9c", "\u5496\u55b1", "\u9ebb\u8fa3", "\u5b5c\u7136", "\u6e05\u6de1", "\u9178\u8fa3", "\u9999\u8fa3", "\u9178\u751c", "\u9999\u9165", "\u5976\u9999", "\u9c7c\u9999", "\u849c\u9999", "\u4e94\u9999", "\u53d8\u6001\u8fa3", "\u6912\u76d0", "\u602a\u5473", "\u751c\u8fa3", "\u723d\u53e3", "\u5fae\u8fa3", "\u9171\u9999", "\u7cdf\u9999", "\u8471\u9999", "\u539f\u5473", "\u869d\u9999", "\u5241\u6912", "\u8d85\u8fa3", "\u4e2d\u8fa3", "\u829d\u58eb\u5473", "\u62b9\u8336\u5473", "\u6ce1\u6912", "\u70e7\u70e4\u5473", "\u54b8\u9c9c", "\u871c\u6c41", "\u849c\u84c9", "\u59dc\u6c41\u5473", "\u9ed1\u6912", "\u8304\u6c41\u5473", "\u7ea2\u6cb9\u5473", "\u7cd6\u918b", "\u9999\u8349\u5473", "\u756a\u8304\u5473", "\u679c\u5473", "\u82a5\u672b\u5473", "\u9ebb\u9171\u5473", "\u8c46\u74e3\u5473", "\u5bb6\u5e38\u5473"], "classify_title": "\u53e3\u5473"},
					{"classify_content": ["\u4e0b\u996d\u83dc", "\u751c\u54c1", "\u8089\u7c7b", "\u4e3b\u98df", "\u79c1\u5bb6\u83dc", "\u51c9\u83dc", "\u70d8\u7119", "\u8c46\u5236\u54c1", "\u7172\u6c64", "\u9152", "\u6d77\u9c9c", "\u6c34\u4ea7", "\u79bd\u7c7b", "\u86cb\u7c7b", "\u51b0\u54c1", "\u996e\u54c1", "\u521b\u610f\u83dc", "\u4e0b\u9152\u83dc", "\u51b0\u6fc0\u51cc", "\u5c0f\u5403", "\u96f6\u98df", "\u9171\u6c41\u4f50\u6599", "\u679c\u9171", "\u706b\u9505", "\u9ebb\u8fa3\u70eb"], "classify_title": "\u83dc\u5f0f"},
					{"classify_content": ["\u7092\u996d", "\u7172\u4ed4\u996d", "\u76d6\u6d47\u996d", "\u7117\u996d", "\u70e9\u996d", "\u7116\u996d", "\u7ca5", "\u5bff\u53f8", "\u997c", "\u7092\u997c", "\u610f\u5927\u5229\u9762", "\u62ab\u8428", "\u9762\u6761", "\u7092\u9762", "\u7116\u9762", "\u51c9\u9762", "\u62cc\u9762", "\u5305\u5b50", "\u9992\u5934", "\u997a\u5b50", "\u9984\u9968", "\u4fbf\u5f53", "\u6cb9\u6761", "\u82b1\u5377", "\u9505\u8d34", "\u7a9d\u5934", "\u76d2\u5b50", "\u53d1\u7cd5", "\u4e09\u660e\u6cbb", "\u6c49\u5821", "\u9995", "\u9505\u76d4", "\u7389\u7c73\u997c", "\u5377\u997c", "\u6cb3\u7c89", "\u7c73\u7c89", "\u7c73\u7ebf", "\u8089\u5939\u998d"], "classify_title": "\u4e3b\u98df"},
					{"classify_content": ["\u9762\u5305", "\u997c\u5e72", "\u621a\u98ce\u86cb\u7cd5", "\u6ce1\u8299", "\u86cb\u7cd5\u5377", "\u676f\u5b50\u86cb\u7cd5", "\u829d\u58eb\u86cb\u7cd5", "\u9a6c\u82ac", "\u66f2\u5947", "\u5410\u53f8", "\u6d77\u7ef5\u86cb\u7cd5", "\u6155\u65af\u86cb\u7cd5", "\u5976\u6cb9\u86cb\u7cd5", "\u78c5\u86cb\u7cd5", "\u5c0f\u86cb\u7cd5", "\u7ffb\u7cd6\u86cb\u7cd5", "\u6b27\u5f0f\u86cb\u7cd5", "\u6d3e", "\u631e", "\u86cb\u631e", "\u9a6c\u5361\u9f99", "\u4e2d\u5f0f\u7cd5\u70b9", "\u6708\u997c"], "classify_title": "\u70d8\u7119"},
					{"classify_content": ["\u70e4\u7bb1\u98df\u8c31", "\u9762\u5305\u673a\u98df\u8c31", "\u7535\u996d\u7172\u7f8e\u98df", "\u8c46\u6d46\u673a\u98df\u8c31", "\u5fae\u6ce2\u7089\u98df\u8c31", "\u7535\u997c\u94db\u98df\u8c31", "\u9ad8\u538b\u9505\u98df\u8c31", "\u7a7a\u6c14\u70b8\u9505\u98df\u8c31", "\u539f\u6c41\u673a\u98df\u8c31", "\u5854\u5409\u9505\u98df\u8c31", "\u4e50\u8475\u6599\u7406\u76d2", "\u84b8\u7bb1\u98df\u8c31", "\u7535\u538b\u529b\u9505"], "classify_title": "\u53a8\u623f\u5de5\u5177"},
					{"classify_content": ["\u65e9\u9910\u98df\u8c31", "\u5348\u9910", "\u4e0b\u5348\u8336", "\u665a\u9910", "\u5bb5\u591c", "\u5355\u8eab\u98df\u8c31", "\u4e8c\u4eba\u4e16\u754c", "\u670b\u53cb\u805a\u9910", "\u6237\u5916\u91ce\u708a", "\u751f\u65e5\u805a\u4f1a", "\u4e00\u5bb6\u4e09\u53e3"], "classify_title": "\u573a\u666f"},
					{"classify_content": ["\u5a74\u513f\uff086-8\u4e2a\u6708\uff09", "\u5a74\u513f\uff088-10\u4e2a\u6708\uff09", "\u5a74\u513f\uff0810-12\u4e2a\u6708\uff09", "\u5e7c\u513f\u98df\u8c31", "\u5b66\u9f84\u524d", "\u513f\u7ae5", "\u9752\u5c11\u5e74", "\u5b55\u5987\u98df\u8c31", "\u4ea7\u5987\u98df\u8c31", "\u6708\u5b50\u9910", "\u66f4\u5e74\u671f", "\u8001\u5e74\u98df\u8c31", "\u61d2\u4eba\u98df\u8c31", "\u7ecf\u671f", "\u7d20\u98df\u4e3b\u4e49", "\u9ad8\u8003\u98df\u8c31", "\u8003\u751f", "\u91cd\u4f53\u529b", "\u5e94\u916c\u4eba\u7fa4", "\u767d\u9886", "\u6559\u5e08", "\u53f8\u673a"], "classify_title": "\u4eba\u7fa4"},
					{"classify_content": ["\u51cf\u80a5\u98df\u8c31", "\u7f8e\u767d\u98df\u8c31", "\u6392\u6bd2\u517b\u989c", "\u7d27\u81f4\u808c\u80a4", "\u4e30\u80f8", "\u795b\u75d8\u795b\u6591", "\u5ef6\u7f13\u8870\u8001", "\u5065\u5eb7\u98df\u8c31"], "classify_title": "\u7f8e\u5bb9\u7626\u8eab"},
					{"classify_content": ["\u8865\u7852\u98df\u8c31", "\u8865\u9499\u98df\u8c31", "\u8865\u950c\u98df\u8c31", "\u8865\u94c1\u98df\u8c31", "\u8865\u7898\u98df\u8c31", "\u5bf9\u6297\u96fe\u973e", "\u9632\u8f90\u5c04", "\u6da6\u80a0\u901a\u4fbf", "\u660e\u76ee", "\u6da6\u80ba\u6b62\u54b3", "\u75db\u7ecf", "\u795b\u6e7f", "\u4fdd\u809d\u8865\u8840", "\u6297\u764c", "\u6ecb\u9634\u58ee\u9633", "\u8c03\u8282\u5185\u5206\u6ccc", "\u8865\u80be", "\u79cb\u51ac\u8fdb\u8865", "\u9a71\u5bd2\u6696\u8eab", "\u6d88\u6691\u89e3\u6e34", "\u6e05\u70ed\u53bb\u706b", "\u517b\u53d1", "\u6d88\u98df", "\u5065\u813e\u517b\u80c3", "\u589e\u8fdb\u98df\u6b32", "\u63d0\u9ad8\u514d\u75ab", "\u51cf\u538b", "\u517b\u5fc3", "\u50ac\u4e73", "\u56de\u5976", "\u589e\u91cd\u589e\u808c", "\u589e\u5f3a\u8bb0\u5fc6\u529b"], "classify_title": "\u529f\u6548"},
					{"classify_content": ["\u964d\u8840\u538b", "\u964d\u8840\u8102", "\u964d\u8840\u7cd6", "\u9aa8\u8d28\u758f\u677e", "\u4fbf\u79d8", "\u8179\u6cfb", "\u8d2b\u8840", "\u5931\u7720", "\u53e3\u8154\u6e83\u75a1", "\u611f\u5192\u53d1\u70e7", "\u8102\u80aa\u809d", "\u75db\u98ce", "\u76ae\u708e", "\u591c\u76f2\u75c7", "\u5e72\u773c\u75c7"], "classify_title": "\u75be\u75c5\u8c03\u7406"},
					{"classify_content": ["\u5e74\u591c\u996d", "\u814a\u516b", "\u5143\u5bb5\u8282", "\u6e05\u660e", "\u7aef\u5348\u8282", "\u4e03\u5915", "\u4e2d\u79cb\u8282", "\u7acb\u79cb", "\u60c5\u4eba\u8282", "\u5723\u8bde\u8282", "\u611f\u6069\u8282", "\u4e07\u5723\u8282"], "classify_title": "\u8282\u65e5/\u65f6\u4ee4"}
				]
	def start_requests(self):
		for classify in self.calssifies:
			classify_content = classify.get('classify_content')
			classify_title = classify.get('classify_title')
			for classify_sub in classify_content:
				classify_raw = classify_sub.decode('unicode_escape')
				url = self.base_url + '/caipu/' + classify_raw
				yield Request(url, self.parse)
				break

	def parse(self, response):
		douguo_bs = BeautifulSoup(response.text,'lxml')
		douguo_container_cp_box = douguo_bs.find_all('div', class_ = 'cp_box')

		for cp_box in douguo_container_cp_box:
			cp_box_a = cp_box.find('a')
			if cp_box_a['href'] != None:
				cp_box_a_href = cp_box_a['href']
				yield Request(cp_box_a_href, RecipesParse().recipesDetail)

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