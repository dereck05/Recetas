from flask import Flask,request
import paramiko
import boto3
from io import *
from multiprocessing.pool import ThreadPool

import psycopg2
import os


app = Flask(__name__)

DATABASE_URL = os.environ['DATABASE_URL']
try:
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    print('conectado')
except:
    "No se puede conectar"







#Regla general: En todos los strings que sean parte de una direccion web, los espacios se representan como  -



@app.route('/cargar')
def carga():
    s3 = boto3.resource('s3')
    data = open('base.pl', 'rb')
    s3.Bucket('progralenguajes').put_object(Key='base.pl', Body=data)
    return 'Hola chicas soy el API:)!'

@app.route('/agregarReceta',methods=['GET','POST'])
def agregarReceta():
    receta = str(request.args.get('receta').replace('-',' '))       #pendiente
    s3 = boto3.resource('s3')
    file = s3.Object('progralenguajes','base.pl').get()['Body'].read()
    string = receta.encode('utf-8')
    str2 = file+string
    io = BytesIO()
    io.write(str2)
    s3.Bucket('progralenguajes').put_object(Key='base.pl',Body=io.getvalue())
    return 'Modified'

@app.route('/buscar',methods=['GET','POST'])
def buscar():
    nombre= str(request.args.get('nombre').replace('-',' '))            #obtiene el string nombre de la direccion HTTP
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('40.117.154.143', 22, 'dereck', 'Progralenguajes123')   #conecta la maquina virtual
    s3 = boto3.resource('s3')
    file = s3.Object('progralenguajes', 'base.pl').get()['Body'].read().decode().replace('\n', '')
    entrada, salida, error = ssh.exec_command('python prolog.py' + " '" + nombre + "' " + '"' + file + '"')
    res= salida.read().decode()
    ssh.close()
    return res



@app.route('/agregarUsuario',methods=['GET','POST'])
def agregarUsuario():                                   #tabla usuario
    correo1 = str(request.args.get('correo'))
    password1 = str(request.args.get('password'))
    cursor = conn.cursor()

    try:

        cursor.execute("""INSERT INTO usuario(correo,password) VALUES(%s,%s);""",(correo1,password1))
        conn.commit()
        cursor.close()
        return "Usuario Registrado"
    except:

        conn.rollback()
        return "El usuario ya se encuentra registrado"

@app.route('/login',methods=['GET','POST'])
def login():
    correo1 = str(request.args.get('correo'))
    password1 = str(request.args.get('password'))
    cursor = conn.cursor()
    cursor.execute("SELECT usuario.password FROM usuario WHERE usuario.correo LIKE %s",(correo1,))
    cu = cursor.fetchone()[0]
    if cu == password1:
        print(cu)
        return 'Login exitoso'
    else:
        return 'Fallo login'



@app.route('/listarTodo',methods=['GET','POST'])
def todasRecetas():
    from pyswip import Prolog
    prolog = Prolog()
    s3 = boto3.resource('s3')
    file = s3.Object('progralenguajes', 'base.pl').get()['Body'].read().decode().replace('\n', '')
    lis = enlistarHechos(file)
    cont = 0
    while (cont < len(lis)):
        prolog.assertz(lis[cont])
        cont += 1

    res=[]

    for i in (prolog.query('comida(A,B,C,D,E)')):
        res.append(list(i))



    return str(res)

@app.route('/buscarNombre',methods=['GET','POST'])
def buscarNombre():
    return 'Exito'
@app.route('/buscarTipo',methods=['GET','POST'])
def buscarTipo():
    return 'Exito'

@app.route('/buscarIngrediente',methods=['GET','POST'])
def buscarIngrediente():
    return 'Exito'



@app.route('/')
def exa():
    return 'Soy el API'

def enlistarHechos(file):
    cont = 0
    rule = ""
    lis = []
    while (cont < len(file)):
        while (file[cont] != '.'):
            rule += file[cont]
            cont += 1
        lis.append(rule)
        cont += 1
        rule = ""

    return lis

if __name__ == '__main__':

    app.run()


