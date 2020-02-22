from .validation_result import ValidationResponse, ValidationError
from mwparserfromhell.nodes import Template
from .single_validator import SingleValidator

CHAMPION_ARGS = [ 'blueban1', 'blueban2', 'blueban3', 'blueban4', 'blueban5', 'red_ban1', 'red_ban2', 'red_ban3', 'red_ban4', 'red_ban5', 'bluepick1', 'bluepick2', 'bluepick3', 'bluepick4', 'bluepick5', 'red_pick1', 'red_pick2', 'red_pick3', 'red_pick4', 'red_pick5' ]

ROLE_ARGS_BLUE = [ 'bluerole1', 'bluerole2', 'bluerole3', 'bluerole4', 'bluerole5' ]
ROLE_ARGS_RED = [ 'red_role1', 'red_role2', 'red_role3', 'red_role4', 'red_role5' ]

VALUES_TO_IGNORE = ['', 'unknown', 'none', 'missing data', 'loss of ban']


class PickBanValidator(SingleValidator):
	def __init__(self, site, cache):
		super().__init__(site, cache)
		self.recognized_templates = ['PicksAndBansS7', 'PicksAndBans']
	
	def validate(self, template: Template):
		response = ValidationResponse()
		response.add_result_if_error(self._has_champion_error(template))
		response.add_result_if_error(self._has_role_error(template))
		return response
	
	def _has_champion_error(self, template):
		values = self._get_values_to_check(CHAMPION_ARGS, template)
		if self._check_for_duplicates(values, 'Champion', length='link'):
			return ValidationError(code='ChampionError')
		return None
	
	def _has_role_error(self, template):
		values = self._get_values_to_check(ROLE_ARGS_BLUE, template)
		if self._check_for_duplicates(values, 'Role', length='role'):
			return ValidationError(code='RoleError')
		values = self._get_values_to_check(ROLE_ARGS_RED, template)
		if self._check_for_duplicates(values, 'Role', length='role'):
			return ValidationError(code='RoleError')
		return None
	
	@staticmethod
	def _get_values_to_check(arg_list, template):
		values = []
		for arg in arg_list:
			if template.has(arg):
				values.append(template.get(arg).value.strip())
		return values
	
	def _check_for_duplicates(self, values, file, length="link"):
		already_seen = []
		for value in values:
			new = self.cache.get_value(file, value, length)
			if new in already_seen:
				return True
			already_seen.append(new)
		return False
