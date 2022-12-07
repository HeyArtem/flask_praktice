from flask import Flask, abort, request, render_template, url_for, redirect
import random
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


'''
Различные примеры flask из разных источников
'''

app = Flask(__name__)
# позволяет славянский шрифт (когда вывод без html)
app.config['JSON_AS_ASCII'] = False

# устанавливаю значение БД с которой буду работать
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

# создание объекта db
db = SQLAlchemy(app)


# декоратор ('это базовый или отцовский) route используется, чтобы связать URL адрес (http://127.0.0.1:5000/)  с функцией
@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/about")
def about():
    return render_template("about.html")


# about_me = {
#    "name": "Артем",
#    "surname": "Рожков",
#    "email": "artem_white@mail.ru"
# }


# # возвращает словарь about_me
# @app.route("/about")
# def about():
#    return about_me


art_lite_dict = {
    'avto': 'Lexus',
    'side': 'South',
    'color': 'Red',
}


# возвращает art_lite_dict
@app.route("/art")
def art_lite():
   return art_lite_dict



# создаю класс который будет представлять табличку в базе данных
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # когда буду выбирать объект, то буду получать и объект и id
    def __repr__(self) -> str:
        return '<Article %r>' % self.id     # !! переделать на нов f row


# создание поста
@app.route("/create-article", methods=["POST", "GET"])
def create_article():
    print("\n", "create_article start")

    # принимаю данные из формы
    if request.method == "POST":
        title = request.form["title"]
        intro = request.form["intro"]
        text = request.form["text"]

        # передаю данные в экземпляр класса
        article = Article(title=title, intro=intro, text=text)

        print("create_article: ", article)

        # сохраняю в БД
        try:
            db.session.add(article) #добавляю
            db.session.commit() #сохраняю
            return redirect("/posts") #переадресовываю пользователя на главную страницу
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template("create-article.html")


# Вывод всех постов
@app.route("/posts")
def posts():

    # # получение первой записи из БД
    # articles = Article.query.first()

    # # получить все записи из БД
    # articles = Article.query.all()
    
    # # все посты + сортировка по дате (по возрастанию)
    # articles = Article.query.order_by(Article.date).all()

    # все посты + сортировка по дате (по убыванию)
    articles = Article.query.order_by(Article.date.desc()).all()

    return render_template("posts.html", articles=articles)


# вывод конкретного поста
@app.route("/posts/<int:id>")
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


# удаление поста. get_or_404-работает, как get, но в случае отсутствия поста укажет 404
@app.route("/posts/<int:id>/del")
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/posts")
    except:
        return "При удалении статьи произошла ошибка"


# редактирование поста
@app.route("/posts/<int:id>/update", methods=["POST", "GET"])
def post_update(id):
    article = Article.query.get(id)

    # принимаю данные из формы
    if request.method == "POST":
        article.title = request.form["title"]
        article.intro = request.form["intro"]
        article.text = request.form["text"]

        try:
            db.session.commit() #сохраняю
            return redirect("/posts") #переадресовываю пользователя на главную страницу
        except:
            return "При редактировании статьи произошла ошибка"            
    else:        
        return render_template("post_update.html", article=article)


# пример вычленение name & id из url
@app.route("/user/<string:name>/<int:id>")
def user(name, id):
    return "User page: " + name + "--" + str(id)


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


# вывод цитат через html в templates
@app.route("/quotes")
def get_all_quotes():   
   return render_template('main.html', data = quotes)


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


'''
перехожу во postman, создаю запросЫ

вывод цитат:
    GET 
    http://127.0.0.1:5000/quotes    

добавление новой цитаты:
    post-запрос создания новой цитаты:
    http://127.0.0.1:5000/quotes
    body-raw-json
    {
    "author": "Pushkin",
    "text": "Text Pushkin Text Pushkin Text Pushkin "
    }

удаление цитаты:
    DELETE
    http://127.0.0.1:5000/quotes/(номер удаляемой цитаты)


POST — создание объекта и отправка данных на сервер;
GET — получение информации с сервера;
PUT — обновление объекта;
DELETE — удаление объекта.
'''

# # вывод цитат без использования стилей и для PostMan (выше есть вывоод на html)
# @app.route("/quotes")
# def get_all_quotes():
#    return quotes


# создание новой цитаты через postman
# @app.route("/quotes", methods=['POST'])
@app.post("/quotes")    # Втрой способ написания хэндлера!!!
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


# создание новой цитаты через форму на html странице
@app.post("/quotes_form")
def create_post_site():
    author = request.form["author"]
    text = request.form["text"]

    last_id = quotes[-1]["id"]
    new_id = last_id + 1

    new_quotes = {
        "id": new_id,
        "author": author,
        "text": text
    }

    quotes.append(new_quotes)
    return render_template("new_quote.html", data=new_quotes)


# удаление цитаты через postman
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
   