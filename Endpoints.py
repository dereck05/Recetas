from flask import Flask,request
import paramiko
import boto3
from io import *
import pickle
import json
import psycopg2
import os
import uuid

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
    return 'cargado'

@app.route('/agregarReceta',methods=['GET','POST'])
def agregarReceta():
    receta = "\n"+str(request.args.get('receta').replace('-',' '))+"\n"
    auth = str(request.args.get('auth'))

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT count(usuario.key) FROM usuario WHERE usuario.key LIKE %s", (auth,))
        cu = cursor.fetchone()[0]
        if(cu == 1):
            s3 = boto3.resource('s3')
            file = s3.Object('progralenguajes','base.pl').get()['Body'].read()
            string = receta.encode('utf-8')
            str2 = file+string
            io = BytesIO()
            io.write(str2)
            s3.Bucket('progralenguajes').put_object(Key='base.pl',Body=io.getvalue())
            return 'Modified'
        else:
            return "No autenticado"
    except:
        conn.rollback()
        return"Error"

@app.route('/detalleReceta',methods=['GET','POST'])
def detalleReceta():
    nombre= str(request.args.get('nombre').replace('-',' '))            #obtiene el string nombre de la direccion HTTP
    auth = str(request.args.get('auth'))
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT count(usuario.key) FROM usuario WHERE usuario.key LIKE %s", (auth,))
        cu = cursor.fetchone()[0]
        if (cu == 1):
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('40.117.154.143', 22, 'dereck', 'Progralenguajes123')   #conecta la maquina virtual
            s3 = boto3.resource('s3')
            file = s3.Object('progralenguajes', 'base.pl').get()['Body'].read().decode().replace('\n', '')
            entrada, salida, error = ssh.exec_command('python prolog.py' + " '" + nombre + "' " + '"' + file + '"')
            res= salida.read().decode()
            ssh.close()
            return res
        else:
            return "No autenticado"
    except:
        conn.rollback()
        return "Error"


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
    try:
        cursor.execute("SELECT usuario.password FROM usuario WHERE usuario.correo LIKE %s",(correo1,))
        cu = cursor.fetchone()[0]
        auth = str(uuid.uuid4())  #Genera un UUID que es el auth key
        if cu == password1:
            try:
                sql_update_query = """UPDATE usuario SET key = (%s) WHERE password LIKE (%s)"""
                cursor.execute(sql_update_query, (auth, cu))
                conn.commit()
                cursor.close()

                return auth
            except:
                conn.rollback()

                return "No autenticado"

        else:
            return 'Fallo login'
    except:
        conn.rollback()
        return 'Fallo login'



@app.route('/listarTodo',methods=['GET','POST'])
def todasRecetas():
    auth = str(request.args.get('auth'))
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT count(usuario.key) FROM usuario WHERE usuario.key LIKE %s", (auth,))
        cu = cursor.fetchone()[0]
        if (cu == 1):
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('40.117.154.143', 22, 'dereck', 'Progralenguajes123')  # conecta la maquina virtual
            s3 = boto3.resource('s3')
            file = s3.Object('progralenguajes', 'base.pl').get()['Body'].read().decode().replace('\n', '')
            entrada, salida, error = ssh.exec_command('python getAll.py' + ' "' + file + '" ')
            x = salida.read().decode()
            return x
        else:
            return "No autenticado"
    except:
        conn.rollback()
        return "Error"

@app.route('/buscarNombre',methods=['GET','POST'])
def buscarNombre():
    nombre = str(request.args.get('nombre').replace('-', ' '))
    auth = str(request.args.get('auth'))
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT count(usuario.key) FROM usuario WHERE usuario.key LIKE %s", (auth,))
        cu = cursor.fetchone()[0]
        if (cu == 1):
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('40.117.154.143', 22, 'dereck', 'Progralenguajes123')  # conecta la maquina virtual
            s3 = boto3.resource('s3')
            file = s3.Object('progralenguajes', 'base.pl').get()['Body'].read().decode().replace('\n', '')
            entrada, salida, error = ssh.exec_command('python buscarNom.py' + " '" + nombre + "' " + '"' + file + '"')
            x = salida.read().decode()
            return x
        else:
            return "No autenticado"
    except:
        conn.rollback()
        return "Error"

@app.route('/buscarTipo',methods=['GET','POST'])
def buscarTipo():
    tipo = str(request.args.get('tipo').replace('-', ' '))
    auth = str(request.args.get('auth'))
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT count(usuario.key) FROM usuario WHERE usuario.key LIKE %s", (auth,))
        cu = cursor.fetchone()[0]
        if (cu == 1):

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('40.117.154.143', 22, 'dereck', 'Progralenguajes123')  # conecta la maquina virtual
            s3 = boto3.resource('s3')
            file = s3.Object('progralenguajes', 'base.pl').get()['Body'].read().decode().replace('\n', '')
            entrada, salida, error = ssh.exec_command('python buscarTipo.py' + " '" + tipo + "' " + '"' + file + '"')
            x = salida.read().decode()
            return x
        else:
            return "No autenticado"
    except:
        conn.rollback()
        return "Error"

@app.route('/buscarIngrediente',methods=['GET','POST'])
def buscarIngrediente():
    nombre = str(request.args.get('nombre').replace('-', ' '))
    auth = str(request.args.get('auth'))
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT count(usuario.key) FROM usuario WHERE usuario.key LIKE %s", (auth,))
        cu = cursor.fetchone()[0]
        if (cu == 1):

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('40.117.154.143', 22, 'dereck', 'Progralenguajes123')  # conecta la maquina virtual
            s3 = boto3.resource('s3')
            file = s3.Object('progralenguajes', 'base.pl').get()['Body'].read().decode().replace('\n', '')
            entrada, salida, error = ssh.exec_command('python buscarIng.py' + " '" + nombre + "' " + '"' + file + '"')
            x = salida.read().decode()
            return x
        else:
            return "No autenticado"
    except:
        conn.rollback()
        return "Error"

@app.route('/credenciales',methods=['GET','POST'])
def credenciales():
    auth = str(request.args.get('auth'))
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT count(usuario.key) FROM usuario WHERE usuario.key LIKE %s", (auth,))
        cu = cursor.fetchone()[0]
        if (cu == 1):

            cursor2 = conn.cursor()
            cursor2.execute("SELECT aws.var1 FROM aws")
            var1 = cursor2.fetchone()[0]

            cursor3 = conn.cursor();
            cursor3.execute("SELECT aws.var2 FROM aws")
            var2= cursor3.fetchone()[0]

            return var1+","+var2
        else:
            return "No autenticado"
    except:
        conn.rollback()
        return "Error"

@app.route('/')
def root():
    return 'Soy el API de recetas:)'



if __name__ == '__main__':

    app.run()


