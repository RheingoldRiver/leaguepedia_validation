from river_mwclient import EsportsSite
from .cache_manager import Cache
from .pickban_validator import PickBanValidator
from .match_schedule_validator import MatchScheduleValidator

def _get_all_validators(site, cache):
	return [
		PickBanValidator(site, cache),
		MatchScheduleValidator(site, cache)
	]

def _create_new_cache(site):
	return Cache(site)

class TemplateValidator(object):
	"""
	This class handles validation on individual templates that can be done out of larger context.
	The type of template doesn't need to be specified here; we will loop through all recognized
	templates in all validators and perform any supported validation
	"""
	def __init__(self, site:EsportsSite, validators=None, cache=None):
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
