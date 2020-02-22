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
		query_text = '{{#invoke:PrintParsedText|unordered|type=champion|' + '|'.join(values) + '}}'
		if self._run_and_evaluate_query(query_text):
			return ValidationError(code='ChampionError')
		return None
	
	def _has_role_error(self, template):
		values = self._get_values_to_check(ROLE_ARGS_BLUE, template)
		query_text = '{{#invoke:PrintParsedText|unordered|type=role|' + '|'.join(values) + '}}'
		if self._run_and_evaluate_query(query_text):
			return ValidationError(code='RoleError')
		values = self._get_values_to_check(ROLE_ARGS_RED, template)
		query_text = '{{#invoke:PrintParsedText|unordered|type=role|' + '|'.join(values) + '}}'
		if self._run_and_evaluate_query(query_text):
			return ValidationError(code='RoleError')
		return None
	
	@staticmethod
	def _get_values_to_check(arg_list, template):
		values = []
		for arg in arg_list:
			if template.has(arg):
				values.append(template.get(arg).value.strip())
		return values
	
	def _run_and_evaluate_query(self, query_text):
		query_result = self.site.api(
			'parse',
			format='json',
			text=query_text,
			prop='text',
			disablelimitreport=1,
			wrapoutputclass=''
		)
		result = query_result['parse']['text']['*']
		result = result.replace('<p>', '').replace('\n</p>', '')
		result_tbl = result.split(',')
		result_parsed = [x for x in result_tbl if x.lower() not in VALUES_TO_IGNORE]
		return len(result_parsed) != len(set(result_parsed))
