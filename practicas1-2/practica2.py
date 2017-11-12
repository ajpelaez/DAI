from flask import *
import mandelbrot
from random import randint
from pathlib import Path
app = Flask(__name__)

@app.route('/hello')                         # decorador, varia los parametros
def hello_world():                      # I/O de la función
    return '¡Hello world!'

@app.route('/')
def html():
    return '<html>\
        <head>\
          <link rel="stylesheet" href="' + url_for('static', filename='css/style.css') + '">\
       </head>\
       <body>\
          <h1>Sitio web para DAI</h1>\
          <h2>Práctica 2 - Ejercicio 2</h2>\
          <p>En esta web de ejemplo importamos un css y una imagen como contenido estático</p>\
          <img src="' + url_for('static', filename = 'imgs/python_logo.png') +'" width="200px" height="200px" </img>\
       </body>\
    </html>\
    '

#http://localhost:8080/user/juan?apellido=perez
@app.route('/user/<username>')
def showUserName(username):
    parametro1 = request.args.get('apellido')
    return 'Hola ' + username + ' '


@app.errorhandler(404)
def page_not_found(error):
    return 'Página no encontrada.'

@app.route('/imagen')
def image():
    return '<a href="' + url_for('static', filename='imgs/python_logo.png') + '">Imagen de prueba</a>'


#http://localhost:8080/dinamica?x1=-1&y1=-1&x2=1&y2=1&ancho=300
@app.route('/dinamica')
def imagenDinamica():
    x1 = float(request.args.get('x1'))
    x2 = float(request.args.get('x2'))
    y1 = float(request.args.get('y1'))
    y2 = float(request.args.get('y2'))
    ancho = int(request.args.get('ancho'))
    nombre_imagen = "static/imgs/mandel"+str(x1)+str(y1)+str(x2)+str(y2)+str(ancho)+".png"
    nombre_imagen2 = "imgs/mandel"+str(x1)+str(y1)+str(x2)+str(y2)+str(ancho)+".png"
    #sistema de cache
    if Path(nombre_imagen).is_file():
        return '<img src="' + url_for('static', filename = nombre_imagen2) +'" </img>'
    else:
        mandelbrot.renderizaMandelbrot(x1,y1,x2,y2,ancho,200,nombre_imagen)
        return '<img src="' + url_for('static', filename = nombre_imagen2) +'" </img>'



@app.route('/svg')
def svg():
    ancho = str(randint(100, 800))
    alto = str(randint(100, 800))
    tamaño = '<svg height="'+alto+'" width="'+ancho+'">'
    figura = randint(0, 2)
    if figura == 0:
        return tamaño + '<ellipse cx="200" cy="80" rx="100" ry="50"\
                        style="fill:yellow;stroke:purple;stroke-width:2" /></svg>'
    elif figura == 1:
        return tamaño + ' <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" /></svg>'
    else:
        return tamaño + '<rect width="'+ancho+'" height="'+alto+'" style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(0,0,0)" /></svg>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # Modo debug
