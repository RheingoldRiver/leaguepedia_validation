from mwclient import Site
from .pickban import PickBanValidator
from .cache_manager import Cache

def _get_all_validators(site, cache):
	return [
		PickBanValidator(site, cache)
	]

def _create_new_cache(site):
	return Cache(site)

class Validator(object):
	def __init__(self, site:Site, validators=None, cache=None):
		self.site = site
		if cache:
			self.cache = cache
		else:
			self.cache = _create_new_cache(site)
		if validators:
			self.validators = validators
		else:
			self.validators = _get_all_validators(site, self.cache)
	
	def validate(self, template):
		for validator in self.validators:
			# We can safely assume each template can only be validated by one validator
			# Because we'll design validators to do full validation for one type of template
			if validator.can_validate(template):
				return validator.validate(template)
