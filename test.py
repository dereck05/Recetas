
import paramiko
import boto3
def x(nombre):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('40.117.154.143',22,'dereck','Progralenguajes123')
    s3 = boto3.resource('s3')
    file = s3.Object('progralenguajes', 'base.pl').get()['Body'].read().decode().replace('\n', '')
    entrada, salida, error=ssh.exec_command('python prolog.py' + " '" +nombre + "' " +'"'+file+'"')
    print('Salida:',salida.read().decode())
    print('Error:', error.read().decode())
    ssh.close()


def pb():
    from pyswip import Prolog

    prolog=Prolog()
    prolog.assertz('comida(arroz,[hola,soy,juan],como,estas,hoy)')
    x= list(prolog.query("comida(arroz,X,A,W,R)"))
    y = x[0]['X'][1]

    print(y)
x('frijol')








