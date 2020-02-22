from mwparserfromhell.nodes import Template
from mwclient import Site

class SingleValidator(object):
	def __init__(self, site: Site, cache):
		self.site = site
		self.cache = cache
		self.recognized_templates = []
	
	def can_validate(self, template: Template):
		if [_ for _ in self.recognized_templates if template.name.matches(_)]:
			return True
		return False
