import os
import aiohttp
import asyncio
from PIL import Image, ImageDraw, ImageFont
import textwrap

class Quote:
	def __init__(self, quote_text, author_name):
		"""
		:param quote_text: текст цитаты
		:param author_name: имя автора цитаты
		"""
		self._quote_text = quote_text
		self._author_name = author_name

	def _calculate_text_parameters(self):
		"""
		Рассчитывает параметры текста в зависимости от длины цитаты.
		Возвращает размер шрифта, длину строки и количество строк.
		"""
		text_length = len(self._quote_text)

		if text_length < 25:
			return 200, 13, 2
		elif text_length < 30:
			return 180, 15, 2
		elif text_length < 55:
			return 150, 18, 3
		elif text_length < 70:
			return 120, 23, 3
		elif text_length < 110:
			return 100, 28, 4
		elif text_length < 180:
			return 80, 35, 5
		elif text_length < 190:
			return 70, 38, 5
		elif text_length < 268:
			return 65, 44, 6
		elif text_length < 369:
			return 55, 52, 7
		elif text_length < 463:
			return 50, 57, 8
		elif text_length < 582:
			return 45, 64, 9
		elif text_length < 727:
			return 40, 72, 10
		elif text_length < 1000:
			return 35, 82, 12
		elif text_length < 1360:
			return 30, 96, 14
		elif text_length < 1866:
			return 25, 116, 16
		else:
			return None

	async def _download_avatar(self, url, save_path):
		"""
		Загружает изображение аватара по URL асинхронно.
		:param url: URL изображения
		:param save_path: путь для сохранения изображения
		"""
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as response:
				if response.status == 200:
					with open(save_path, 'wb') as f:
						f.write(await response.read())

	async def create(self, folder_name, avatar_name, result_filename, use_url=False,
					 headline_text_font='Formular-Italic.ttf', headline_text_size=100,
					 headline_text='Цитаты мудрых людей', author_name_font='PeridotDemoPE-WideExtraBoldItalic.otf',
					 author_name_size=80, quote_text_font='Formular-BlackItalic.ttf') -> bool:
		"""
		Создает изображение с цитатой и сохраняет его в указанной папке

		:param folder_name: название папки, где находится аватар
		:param avatar_name: название файла с аватаром или URL для загрузки
		:param result_filename: имя итогового файла
		:param use_url: если True, то загружает фото автора по URL
		:return: True, если метод выполнился успешно
		"""

		# Получаем путь к текущей директории, где находится этот файл
		base_path = os.path.dirname(__file__)

		# Формируем пути к шрифтам относительно директории этого файла
		quote_text_font_path = os.path.join(base_path, quote_text_font)
		headline_text_font_path = os.path.join(base_path, headline_text_font)
		author_name_font_path = os.path.join(base_path, author_name_font)

		# Формируем пути к файлам
		save_path = os.path.join(folder_name, result_filename + '_quote.png')

		# Получаем параметры для текста
		text_params = self._calculate_text_parameters()

		# Если параметры равны None, то текст слишком длинный
		if text_params is None:
			print("Текст слишком длинный для создания изображения.")
			return False

		# Извлекаем параметры
		quote_text_size, width, num_lines = text_params

		# Обрезаем и форматируем текст цитаты
		text = '\n'.join(textwrap.wrap(self._quote_text, width=width)[:num_lines])

		# Создание изображения размером 1920x1080
		user_img = Image.new('RGBA', (1920, 1080), color='#000000')
		drawer = ImageDraw.Draw(user_img)

		# Загрузка шрифтов с указанием абсолютных путей
		font_1 = ImageFont.truetype(font=quote_text_font_path, size=quote_text_size, encoding='UTF-8')
		font_2 = ImageFont.truetype(font=headline_text_font_path, size=headline_text_size, encoding='UTF-8')
		font_3 = ImageFont.truetype(font=author_name_font_path, size=author_name_size, encoding='UTF-8')

		# Размер заголовка
		size_headline = drawer.textsize(headline_text, font=font_2)

		# Рисуем заголовок
		drawer.text(((1920 - size_headline[0]) / 2, 50), headline_text, fill='white', font=font_2)

		# Рисуем текст цитаты
		drawer.text((100, 189), f"«{text}»", fill='white', font=font_1)

		# Загружаем фото
		avatar_path = os.path.join(folder_name, avatar_name)

		if use_url:
			# Скачиваем фото по URL асинхронно
			avatar_path = os.path.join(folder_name, "avatar_from_url.jpg")
			await self._download_avatar(avatar_name, avatar_path)

		# Обрезаем фото в круг
		user_photo = Image.open(avatar_path).resize((300, 300), Image.Resampling.LANCZOS).convert("RGBA")
		mask = Image.new('L', (300, 300), 0)
		ImageDraw.Draw(mask).ellipse((0, 0, 300, 300), fill=255)
		user_photo.putalpha(mask)
		user_img.paste(user_photo, (50, 730), mask=user_photo)

		# Вычисляем размер и положение имени автора
		author_name_text = f'© {self._author_name}'
		author_text_size = drawer.textsize(author_name_text, font=font_3)

		# Позиционируем имя автора в центре аватарки, сдвигаем на 50 пикселей вправо
		author_x = 50 + 300 + 50  # 50 пикселей от левого края, 300 - ширина аватарки, еще 50 пикселей для сдвига
		author_y = 730 + (300 // 2) - (author_text_size[1] // 2)  # Центрируем по вертикали

		# Рисуем имя автора
		drawer.text((author_x, author_y), author_name_text, fill='white', font=font_3)

		# Сохраняем изображение
		user_img.save(save_path)

		# Если фото было скачано, удаляем его
		if use_url:
			os.remove(avatar_path)

		return True
