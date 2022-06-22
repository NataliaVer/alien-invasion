import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""Клас, що представляе одного прибульця з флоту"""
	def __init__(self, ai_game):
		"""Ініціалізувати прибульця та задати його початкове розташування"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings

		#Завантаження інопланетне зображення та встановлення його атрибутів
		self.image = pygame.image.load("images/alien.bmp")
		self.rect = self.image.get_rect()

		#Початок кожного нового прибульця зверху зліва екрану
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		#Зберігати точне горизонтальне положення інопланетянина
		self.x = float(self.rect.x)

	def check_edges(self):
		"""Повертає істину, коли прибулець знаходится на краю екрану"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right or self.rect.left <= 0:
			return True
		
	def update(self):
		"""Змістити прибульця праворуч чи ліворуч"""
		self.x += (self.settings.alien_speed *
			self.settings.fleet_direction)
		self.rect.x = self.x