from mwparserfromhell.nodes import Template
from .validation_result import ValidationResponse, ValidationError
from .single_validator import SingleValidator
from .cache_manager import Cache


class MatchScheduleValidator(SingleValidator):
	def __init__(self, site, cache:Cache=None):
		# If this is being called as part of a composite Validator, cache is guaranteed to be defined
		# However, if this is being called on its own we might to let it have its own cache
		super().__init__(site, cache=cache)
		self.recognized_templates = ['MatchSchedule', 'MatchScheduleGame']
		
	def validate(self, template:Template):
		response = ValidationResponse()
		response.add_result_if_error(self._has_winner_key_error(template))
		return response
	
	def _has_winner_key_error(self, template):
		if not template.has('winner'):
			return None
		winner = template.get('winner').value.strip()
		if winner == '':
			return None
		try:
			int(winner)
			return None
		except ValueError:
			return ValidationError(code="InvalidWinner", description="Winner should be 1 or 2, not the name of a team")
