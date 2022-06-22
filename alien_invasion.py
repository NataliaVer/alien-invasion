import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
	"""Загальний клас, що керує ресурсами та поведінкою гри."""
	def __init__(self):
		"""Ініціалізувати гру, створити ресурси гри."""
		pygame.init()
		self.settings = Settings()

		#Режим екрана з заданими розмірами
		self.screen = pygame.display.set_mode(
			(self.settings.screen_width, self.settings.screen_height))
		#Для повноекранного режиму
		# self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		# self.settings.screen_width = self.screen.get_rect().width
		# self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alian Invasion")

		#Створити екземпляр для збереження ігрової статистики
		#та табло на екрані
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		#Додати корабель
		self.ship = Ship(self)
		#Додати групу для куль
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		#метод визиваємо при ініціалізації
		self._creat_fleet()

		#Створити кнопку Play
		#self.play_button = Button(self, "Play")
		self.screen_rect = self.screen.get_rect()
		self.play_button_light = Button(self, "Light")
		self.play_button_hard = Button(self, "Hard")
		self.play_button_hardest = Button(self, "Hardest")


	def run_game(self):
		"""Розпочати головний цикл гри."""
		while True:
			self._check_events()
			if self.stats.game_active:
				self.ship.update()

				self._update_bullets()
				self._update_aliens()

			self._update_screen()


	def _check_events(self):
		"""Слідкувати за подіями миші та клавіатури."""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self._save_record()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._chec_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._chec_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)


	def _save_record(self):
		"""Зберегти рекорд до файлу"""
		#Порівняємо данні і, за потреби, запишемо рекорд гри
		filename = 'record_ai.txt'

		if self.stats.high_score > self.stats.saved_record:
				with open(filename, 'w') as file_object:
					file_object.write(str(self.stats.high_score))

	def _check_play_button(self, mouse_pos):
		"""Розпочати нову гру після натискання кнопки Play"""
		if not self.stats.game_active:
			button_clicked = self.play_button_light.rect.collidepoint(mouse_pos)
			if button_clicked and not self.stats.game_active:
				#Анулювати статистику гри
				self.settings.initialize_dynamic_settings(1)
				#self._start_game()
				#print("Light")
			else:
				button_clicked = self.play_button_hard.rect.collidepoint(mouse_pos)
				if button_clicked and not self.stats.game_active:
					#Анулювати статистику гри
					self.settings.initialize_dynamic_settings(1.4)
					#self._start_game()
					#print("hard")
				else:
					button_clicked = self.play_button_hardest.rect.collidepoint(mouse_pos)
					if button_clicked and not self.stats.game_active:
						#Анулювати статистику гри
						self.settings.initialize_dynamic_settings(1.8)
						#self._start_game()
						#print("hardest")
			self._start_game()



	def _chec_keydown_events(self, event):
		"""Реагувати на натискання клавіш"""
		if event.key == pygame.K_RIGHT:
			#Перемістити корабель праворуч.
			#self.ship.rect.x += 1
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			self._save_record()
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
		elif event.key == pygame.K_p:
			self._start_game()

	def _start_game(self):
		"""Почати гру заново"""
		#Анулювати ігрову статистику
		self.stats.reset_stats()
		self.stats.game_active = True
		self.sb.prep_score()
		self.sb.prep_level()
		self.sb.prep_ships()

		#Позбутися надлишку прибульців та куль
		self.aliens.empty()
		self.bullets.empty()

		#Створити новий флот та відцентрувати корабель
		self._creat_fleet()
		self.ship.center_ship()

		#Приховати курсор миші
		pygame.mouse.set_visible(False)


	def _chec_keyup_events(self, event):
		"""Реагувати, коли клавіша не натиснута"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False


	def _fire_bullet(self):
		"""Створити нову кулю та додати її до групи куль"""
		if self.stats.game_active and len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Оновити позицію куль та позбутися старих куль"""
		#Оновити позиції куль
		self.bullets.update()
		#Позбутися куль, що зникли
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_collisions()

		
	def _check_bullet_alien_collisions(self):
		"""Реакція на зіткнення куль з прибульцями"""
		#Видалити всі кулі та прибільців, що зіткнулися
		collisions = pygame.sprite.groupcollide(
			self.bullets, self.aliens, True, True)

		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()

		if not self.aliens:
			#Знищити наявні кулі та створити новий флот
			self.bullets.empty()
			self._creat_fleet()
			self.settings.increase_speed()

			#Збільшити рівень
			self.stats.level += 1
			self.sb.prep_level()

	def _update_aliens(self):
		"""
		Перевірити, чи флот знаходится на краю,
		тоді оновити позиції всіх прибульців у флоті
		"""
		self._check_fleet_edges()
		self.aliens.update()

		#Шукати зіткнення корабля з прибульцями
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		#Шукати чи котрийсь із прибульців досяг краю екрана
		self._check_aliens_bottom()

	def _creat_fleet(self):
		"""Створити флот прибульців."""
		#Створити прибульців та визначити кількість прибульців у ряду.
		#Відстань між прибульцями = ширині одного прибульця.
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_alients_x = available_space_x // (2 * alien_width)

		#Визначити, яка кількість рядів прибульців поміщаєтся на екрані
		ship_height = self.ship.rect.height
		avialable_space_y = (self.settings.screen_height - 
			(3 * alien_height) - ship_height)
		number_rows = avialable_space_y // (2 * alien_height)

		#Створити повний флот прибульців
		for row_number in range(number_rows):
			#Створити перший ряд прибульців.
			for alien_number in range(number_alients_x):
				self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		"""Створити прибульця, та поставити його до ряду"""
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 *alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2 *alien.rect.height * row_number
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""Реагує відповідно до того, чи досяг котрийсь
		із прибульців краю екрана
		"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Спуск всього флоту та зміна його напрямку"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _ship_hit(self):
		"""Реагувати на зіткнення прибульця з кораблем"""
		if self.stats.ships_left > 0:
			#Зменшити ship_left
			self.stats.ships_left -= 1
			self.sb.prep_ships()

			#Позбутися надлишку прибульців та куль
			self.aliens.empty()
			self.bullets.empty()

			#Створити новий флот та відцентрувати корабель
			self._creat_fleet()
			self.ship.center_ship()

			#Пауза
			sleep(0.5)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _check_aliens_bottom(self):
		"""Перевірити, чи не досяг якийсь прибулець нижнього краю екрану"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				#Зреагувати так ніби корабель було підбито
				self._ship_hit()
				break


	def _update_screen(self):
		"""Наново перемалювати екран на кожній ітерації циклу."""
		self.screen.fill(self.settings.bg_color) # в підручнику self.settings.bg_color
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)

		#Намалювати інформацію про рахунок
		self.sb.show_score()

		#Намалювати кнопку Play, якщо гра неактивна
		if not self.stats.game_active:
			self.play_button_light.draw_button()
			self.play_button_hard.draw_button()
			self.play_button_hardest.draw_button()

		#Показати останній намальований екран.
		pygame.display.flip()


if __name__ == '__main__':
	#Створити екземпляр гри та запустити гру.
	ai = AlienInvasion()
	ai.run_game()
