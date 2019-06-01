'''

def x():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('40.117.154.143',22,'dereck','Progralenguajes123')
    s3 = boto3.resource('s3')
    file = s3.Object('progralenguajes', 'base.pl').get()['Body'].read().decode().replace('\n', '')
    entrada, salida, error = ssh.exec_command('python getAll.py' + ' "' + file + '" ')

    print('Salida:',salida.read().decode())
    print('Error:', error.read().decode())
    ssh.close()



'''
from flask import Flask,request
import paramiko
import boto3
from io import *
import pickle
import json
import psycopg2
import os
import uuid



conn = psycopg2.connect("postgresql://postgres:postgres@localhost/postgres")

print('conectado')



def x():

    correo1 = "de@gmail.com"

    password1 = "hola123"

    cursor = conn.cursor()

    cursor.execute("SELECT a.password FROM a WHERE a.correo LIKE %s", (correo1,))
    cu = str(cursor.fetchone()[0])
    auth = str(uuid.uuid4())  # Genera un UUID que es el auth key
    if cu == password1:
        try:
            #sql_update_query = "UPDATE a set a.key =  where a.password LIKE %s"
            cursor.execute("UPDATE a SET key = ('123') where password LIKE ('qwerty123')")
            conn.commit()
            cursor.close()

            print(auth)
        except:
            conn.rollback()

            print ("Fail")

    else:
        print('Fallo login')


if __name__ == '__main__':


    x()


