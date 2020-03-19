from river_mwclient import EsportsSite
import json

class Cache(object):
	def __init__(self, site: EsportsSite):
		self.cache = {}
		self.site = site
	
	def get_json_lookup(self, filename):
		if filename in self.cache:
			return self.cache[filename]
		result = self.site.api(
			'expandtemplates',
            prop='wikitext',
			text='{{JsonEncode|%s}}' % filename
		)
		self.cache[filename] = json.loads(result['expandtemplates']['wikitext'])
		return self.cache[filename]
	
	def get_value_from_lookup_json(self, filename, key, length):
		"""
		Returrns the length of the lookup of a key requested from the filename requested. Assumes the file has
		the same structure as the -names modules on Leaguepedia.
		:param filename: "Champion", "Role", etc. - the name of the file
		:param key: The lookup key, e.g. "Morde"
		:param length: The length of value to return, e.g. "long" or "link"
		:return: Correct lookup value provided, or None if it's not found
		"""
		file = self.get_json_lookup(filename)
		if key not in file:
			return None
		if not isinstance(file[key], str):
			return file[key][length]
		return file[file[key]][length]
	
	def get_cargo_query(self, key, **kwargs):
		"""
		Cache results of a cargo query and return if needed
		:param key: A key to save this query as to look it up later without rerunning the query
		:param kwargs: Parameters for a cargoquery api call
		:return:
		"""
		if self.cache[key]:
			return self.cache[key]
		result = self.site.cargoquery(**kwargs)
		self.cache[key] = result
		return result
