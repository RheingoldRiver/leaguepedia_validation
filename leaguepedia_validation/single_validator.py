from mwparserfromhell.nodes import Template
from river_mwclient import EsportsSite
from .cache_manager import Cache

class SingleValidator(object):
	def __init__(self, site: EsportsSite, cache:Cache=None):
		self.site = site
		if not cache:
			self.cache = Cache(site)
		self.cache = cache
		self.recognized_templates = []
	
	def can_validate(self, template: Template):
		if [_ for _ in self.recognized_templates if template.name.matches(_)]:
			return True
		return False
