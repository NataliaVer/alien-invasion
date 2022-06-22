class Settings:
	"""Клас для збереження всіх налаштувань гри."""

	def __init__(self):
		"""Ініціалізувати налаштування гри."""
		# Screen settings
		self.screen_width = 1100
		self.screen_height = 600
		self.bg_color = (230, 230, 230)
		
		#Налаштування корабля
		self.ship_limit = 3
		
		#Налаштування кулі
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 5
		
		#Налаштування прибульця
		self.fleet_drop_speed = 10
		
		#Як швидко гра має прискорюватися
		self.speedup_scale = 1.1

		#Як швидко збільшується вартість прибільців
		self.score_scale = 1.5

		self.initialize_dynamic_settings()


	def initialize_dynamic_settings(self, speedup_level=1.0):
		"""Ініціалізація змінних налаштувань"""
		self.ship_speed = 1.5*speedup_level
		self.bullet_speed = 1.5*speedup_level
		self.alien_speed = 1.0*speedup_level

		#fleet_direction 1 означає напрямок руху праворуч -1 -- ліворуч
		self.fleet_direction = 1

		#Отримання балів
		self.alien_points = 50


	def increase_speed(self):
		"""Збільшення налаштувань швидкості та вартості прибульців"""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)
