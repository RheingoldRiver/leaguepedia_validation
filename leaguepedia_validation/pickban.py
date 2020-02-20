CHAMPION_ARGS = [ 'blueban1', 'blueban2', 'blueban3', 'blueban4', 'blueban5', 'red_ban1', 'red_ban2', 'red_ban3', 'red_ban4', 'red_ban5', 'bluepick1', 'bluepick2', 'bluepick3', 'bluepick4', 'bluepick5', 'red_pick1', 'red_pick2', 'red_pick3', 'red_pick4', 'red_pick5' ]

ROLE_ARGS_BLUE = [ 'bluerole1', 'bluerole2', 'bluerole3', 'bluerole4', 'bluerole5' ]
ROLE_ARGS_RED = [ 'red_role1', 'red_role2', 'red_role3', 'red_role4', 'red_role5' ]

VALUES_TO_IGNORE = ['', 'unknown', 'none', 'missing data', 'loss of ban']


class PickBanValidator(object):
	def __init__(self, site, template):
		self.site = site
		self.template = template
	
	def get_values_to_check(self, arg_list):
		values = []
		for arg in arg_list:
			if self.template.has(arg):
				values.append(self.template.get(arg).value.strip())
		return values
	
	def run_and_evaluate_query(self, query_text):
		query_result = self.site.api(
			'parse',
			format='json',
			text=query_text,
			prop='text',
			disablelimitreport=1,
			wrapoutputclass=''
		)
		print(query_result)
		result = query_result['parse']['text']['*']
		result = result.replace('<p>', '').replace('\n</p>', '')
		result_tbl = result.split(',')
		result_parsed = [x for x in result_tbl if x.lower() not in VALUES_TO_IGNORE]
		return len(result_parsed) != len(set(result_parsed))
	
	def has_champion_error(self):
		values = self.get_values_to_check(CHAMPION_ARGS)
		query_text = '{{#invoke:PrintParsedText|unordered|type=champion|' + '|'.join(values) + '}}'
		return self.run_and_evaluate_query(query_text)
	
	def has_role_error(self):
		values = self.get_values_to_check(ROLE_ARGS_BLUE)
		query_text = '{{#invoke:PrintParsedText|unordered|type=role|' + '|'.join(values) + '}}'
		if not self.run_and_evaluate_query(query_text):
			return False
		values = self.get_values_to_check(ROLE_ARGS_RED)
		query_text = '{{#invoke:PrintParsedText|unordered|type=role|' + '|'.join(values) + '}}'
		return self.run_and_evaluate_query(query_text)
