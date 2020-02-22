class ValidationResponse(object):
	def __init__(self):
		self.errors = []
		self.has_errors = False
	
	def add_result_if_error(self, err):
		if err:
			self.errors.append(err)
			self.has_errors = True
	

class ValidationError(object):
	def __init__(self, code:str=None, description:str=None):
		self.code = code
		self.description = description
