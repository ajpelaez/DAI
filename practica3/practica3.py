from flask import *
from pathlib import Path
import shelve

app = Flask(__name__)
app.secret_key = 'A0Zr98alskfokwapfaj/3yX R~XHH!jmN]LWX/,?RT'


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

@app.route('/bucles')
def show_bucles_content():
    update_pages()
    session['current_page'] = "Página bucles"
    return render_template("index.html", content=4)


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



def update_pages():
    if session.get('last_page3'):
        session['last_page4'] = session['last_page3']
    if session.get('last_page2'):
        session['last_page3'] = session['last_page2']
    if session.get('current_page'):
        session['last_page2'] = session['current_page']



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # Modo debug
