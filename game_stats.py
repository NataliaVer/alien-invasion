
class GameStats:
	"""Відстеження статистики гри"""
	def __init__(self, ai_game):
		"""Ініціалізація статистики"""
		self.settings = ai_game.settings
		self.reset_stats()
		#Розпочати гру в активному стані
		self.game_active = False
		#Рекорд не анульовується
		self.high_score = self._open_file_record()
		self.saved_record = self.high_score

	def reset_stats(self):
		"""Ініціалізація статистики, що може зміноватися впродовж гри"""
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 1

	def _open_file_record(self):
		"""Відкрити файл в якому знаходится рекорд гри"""
		filename = 'record_ai.txt'

		try:
			with open(filename) as file_object:
				contents = file_object.read()
		except FileNotFoundError:
			return 0
			print("Not found")
		else:
			try:
				contents = int(contents)
			except ValueError:
				return 0
				print("Not int")
			else:
				return contents