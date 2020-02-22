from mwclient import Site
import json

class Cache(object):
	def __init__(self, site: Site):
		self.cache = {}
		self.site = site
	
	def get_file(self, filename):
		if filename in self.cache:
			return self.cache[filename]
		result = self.site.api(
			'expandtemplates',
            prop='wikitext',
			text='{{JsonEncode|%s}}' % filename
		)
		self.cache[filename] = json.load(result['expandtemplates']['wikitext'])
	
	def get_value(self, filename, key, length):
		"""
		Returrns the length of the lookup of a key requested from the filename requested. Assumes the file has
		the same structure as the -names modules on Leaguepedia.
		:param filename: "Champion", "Role", etc. - the name of the file
		:param key: The lookup key, e.g. "Morde"
		:param length: The length of value to return, e.g. "long" or "link"
		:return: Correct lookup value provided, or None if it's not found
		"""
		file = self.get_file(filename)
		if key not in file:
			return None
		if type(file[key]) != 'str':
			return file[key][length]
		return file[file[key]][length]
