from flask import *
from pathlib import Path
import shelve
from bson.json_util import dumps
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'A0Zr98alskfokwapfaj/3yX R~XHH!jmN]LWX/,?RT'
client = MongoClient()


@app.route('/')
def index():
    return render_template("index.html", content=1)

@app.route('/variables')
def show_variables_content():
    update_pages()
    session['current_page'] = "Página variables"
    return render_template("index.html", content=1)

@app.route('/listas')
def show_lists_content():
    update_pages()
    session['current_page'] = "Página listas"
    return render_template("index.html", content=2)

@app.route('/funciones')
def show_functions_content():
    update_pages()
    session['current_page'] = "Página funciones"
    return render_template("index.html", content=3)

@app.route('/restaurantes', methods=['GET', 'POST'])
def show_restaurants_content():
    update_pages()
    session['current_page'] = "Página restaurantes"
    if request.method == 'GET':
        tipos_cocina_disponibles = get_restaurants_values('cuisine')
        barrios_disponibles = get_restaurants_values('borough')
        return render_template("index.html", content=4,
                tipos_cocina=tipos_cocina_disponibles, barrios = barrios_disponibles)
    else:
        restaurantes_encontrados = search_restaurants(request.form['cocina'],request.form['barrio'])
        return render_template("index.html", content=4, busqueda_realizada=True,
                restaurantes=restaurantes_encontrados)

@app.route('/restaurantes-ajax')
def show_restaurants_ajax():
    update_pages()
    session['current_page'] = "Página restaurantes"
    tipos_cocina_disponibles = get_restaurants_values('cuisine')
    barrios_disponibles = get_restaurants_values('borough')
    return render_template("index.html", content=5,
            tipos_cocina=tipos_cocina_disponibles, barrios = barrios_disponibles)


@app.route('/logout')
def logout():
    session.clear()
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = shelve.open("shelve.db")
        if username in db:
            if db[username] == password:
                session['username'] = username
                db.close()
                return render_template("index.html")
            else:
                db.close()
                return render_template("index.html")
        else:
            db[username] = password
            db.close()
            session['username'] = username
            return render_template("index.html")
    else:
        return render_template("index.html")


@app.route('/get-restaurants/<cocina>/<barrio>')
def get_restaurants(cocina,barrio):
    return search_restaurants2(cocina,barrio)

@app.route('/get-restaurants/<cocina>/<barrio>/<numero_restaurantes>')
def get_restaurants2(cocina,barrio,numero_restaurantes):
    return search_restaurants2(cocina,barrio,int(numero_restaurantes))

def update_pages():
    if session.get('last_page3'):
        session['last_page4'] = session['last_page3']
    if session.get('last_page2'):
        session['last_page3'] = session['last_page2']
    if session.get('current_page'):
        session['last_page2'] = session['current_page']

def search_restaurants2(tipo_cocina, barrio, skip=0):
    db = client.test
    cursor = db.restaurants.find({"cuisine": tipo_cocina, "borough": barrio}).limit(10).skip(skip)
    data = []
    for restaurante in cursor:
        print(restaurante)
        data.append({"name" : restaurante["name"],
            "address" : restaurante["address"]["street"],
            "grade" : restaurante["grades"][0]["grade"]
        })
    return jsonify(data)

def search_restaurants(tipo_cocina, barrio, skip=0):
    db = client.test
    cursor = db.restaurants.find({"cuisine": tipo_cocina, "borough": barrio}).limit(10).skip(skip)
    return cursor

def get_restaurants_values(restaurant_info):
    db = client.test
    cursor = db.restaurants.distinct(restaurant_info)
    return cursor

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # Modo debug
