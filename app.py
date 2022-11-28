from flask import Flask, abort, request
import random
import sqlite3


# урок с Данилой
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


quotes = [
   {
       "id": 1,
       "author": "Rick Cook",
       "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает."
   },
   {
       "id": 2,
       "author": "Waldi Ravens",
       "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
   },
   {
       "id": 3,
       "author": "Mosher’s Law of Software Engineering",
       "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
   },
   {
       "id": 4,
       "author": "Yoggi Berra",
       "text": "В теории, теория и практика неразделимы. На практике это не так."
   },

]


# декоратор ('это базовый или отцовский) route используется, чтобы связать URL адрес (http://127.0.0.1:5000/)  с функцией
@app.route("/")
def hello_world():
    return "Hello, World!"


about_me = {
   "name": "Артем",
   "surname": "Рожков",
   "email": "artem_white@mail.ru"
}


@app.route("/about")
def about():
   return about_me


art_lite_dict = {
    'avto': 'Lexus',
    'side': 'South',
    'color': 'Red',
}


# url = /art
@app.route("/art")
def art_lite():
   return art_lite_dict

# вывод цитат
@app.route("/quotes")
def get_all_quotes():
   return quotes


# счетчик количества цитат. Внимание в url идет корневой каталог(quotes)/объект с которым работаем(digital)/digital
@app.route("/quotes/digital")
def get_all_quotes_digital():
    return {
        "digital": len(quotes)
    }


# вывод рандомных цитат
@app.route("/quotes/random")  
def get_all_quotes_random():
    # return random.choice(quotes)
    return random.choice(quotes)

# возврещение цитаты по id, использую ХИНТИНГ 
# чтобы прервать запрос с кодом ошибки используйте функцию abort()
@app.route("/quotes/<int:id>")
def get_quote(id):
    for quote in quotes:
        if quote["id"] == id:
            return quote
    abort(404, f"Цитата {id} не найдена")


# создание новой цитаты
# в postman, создаю запросЫ
@app.route("/quotes", methods=['POST'])
def created_post():
    new_quote = request.json    

    # id последней цитаты
    last_id = quotes[-1]["id"]

    # добавляю id новой цитаты
    new_quote["id"] = last_id + 1

    # записываю новую цитату
    quotes.append(new_quote)
    
    # print(type(new_quote))
    return new_quote, 201


'''
перехожу во postman, создаю запросЫ

GET http://127.0.0.1:5000/quotes    

post-запрос создания новой цитаты:
POST http://127.0.0.1:5000/quotes
body raw json
    {
    "author": "Pushkin",
    "text": "Text Pushkin Text Pushkin Text Pushkin "
    }


POST — создание объекта и отправка данных на сервер;
GET — получение информации с сервера;
PUT — обновление объекта;
DELETE — удаление объекта.
'''

# # удаление цитаты
# @app.route("/quotes/<int:id>", methods=['DELETE'])
# def delete_post(id):
#     for quote in quotes[id]:
#         abort(404, f"Указанного id= {id}, не существует.")
#         if id == quote["id"]:
#             quotes.remove(quote)
#             return f"Цитата {'id'} удалена", 200 

@app.route("/quotes/<int:id>", methods=['DELETE'])
# @app.delete("/quotes/<int:id>")   # второй вариант написания хэндлера,без прописывания methods=['DELETE']
def delete_post(id):    
    for quote in quotes:       
        if id == quote["id"]:
            quotes.remove(quote)
            return f"Цитата {id} удалена", 200
         # выполняется abort & python дальше не думет
    abort(404, f"Указанного id= {id}, не существует")
    

   
    
    
    



      









def main():
    app.run(debug=True) #debug=True - включен режим отладки (как будто перезагружать не нужно после изменения, так же будет отчет об ошипбке на HTML-СТРАНИЦЕ)


if __name__ == "__main__":
    main()
   