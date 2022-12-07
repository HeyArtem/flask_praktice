from flask import Flask, render_template, request

'''
урок UAI
'''


# создал сервер
app = Flask(__name__)


@app.route("/flask")
@app.route("/")
def hello_world():
    return "Hello, World!"


#  с помомощью метода render templates (импортировать), свяжу функцию с uia_main.html
@app.route("/main")
def main():
    return render_template('uai_main.html')    


@app.route("/contacts")
def contacts():

    # # вар 1
    # model = 'Volvo'
    # price = 1.5
    # return render_template('uai_contacts.html', model = model, price = price)

    # вар 2 пердаю данные на uai_contacts.html в виде dict
    data = {
        'model': 'Volvo',
        'price': 1.5
    }
    return render_template('uai_contacts.html', data = data)


@app.route("/moto")
def moto():
    data = {
        'model': 'BMW',
        'price': 0.8
    }
    return render_template('uai_moto.html', **data)     #новая форма передачи (словарь)


# заполнение формы
@app.route("/cars_form", methods = ["POST"]) 
def cars_form():
    brand = request.form["brand"]
    price = request.form["price"]

    # print(brand, price)

    data_f = {
        'model': brand,
        'price': price
    }
    return render_template('uai_forms_cars.html', data=data_f)





def main():
    app.run(debug=True) #debug=True - включен режим отладки (как будто перезагружать не нужно после изменения, так же будет отчет об ошипбке на HTML-СТРАНИЦЕ)


if __name__ == "__main__":
    main()
   