from river_mwclient.esports_site import EsportsSite
from mwparserfromhell import wikicode, parse
from mwclient.page import Page
from .template_validator import TemplateValidator
from .cache_manager import Cache

class Validator(object):
	site = None
	cache = None
	template_validator = None
	errors = []
	def __init__(self, site: EsportsSite=None, cache:Cache=None,
	             template_validator: TemplateValidator=None):
		self.site = site
		if not cache:
			cache = Cache(site)
		self.cache = cache
		if not template_validator:
			template_validator = TemplateValidator(site, cache=cache)
		self.template_validator = template_validator
		
	def validate(self, wikitext:wikicode=None, title:str=None, page:Page=None):
		if not wikitext and not title and not page:
			return
		if title and not page:
			page = self.site.client.pages[title]
		if not wikitext:
			wikitext = parse(page.text())
		template_indices = {}
		for template in wikitext.filter_templates():
			if template not in template_indices:
				template_indices[template] = 0
			template_indices[template] += 1
			errors = self.template_validator.validate(template)
			if not errors:
				continue
