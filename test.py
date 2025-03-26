import asyncio
from simpledemotivators import Quote  # Импортируем класс Quote

async def main():
    quote = Quote("Ну типа цитата", "Hinaichigo_fox")
    #quote = Quote("Текст", "Автор")
    folder_name = "/citgen/"  # Папка для изображений
    avatar_name = "123.jpg"  # Название файла с аватаром
    avatar_url = "https://img.booru.org/rm//images/125/39c666e7e7baab8e39789f1d7089f4b390ee6505.jpg" #если надо скачать
    result_filename = "quote_url"  # Имя итогового файла
    result_filename_photo = "quote_photo"  # Имя итогового файла

    # вызываем метод. Первое делает по url второе локально
    success = await quote.create(folder_name=folder_name, avatar_name=avatar_url, result_filename=result_filename, use_url=True)
    success = await quote.create(folder_name=folder_name, avatar_name=avatar_name, result_filename=result_filename_photo)

    if success:
        print("Цитата успешно создана!")
    else:
        print("Не удалось создать цитату.")

if __name__ == "__main__":
    asyncio.run(main())