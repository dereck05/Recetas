
import paramiko
import boto3
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


def pb():
    '''
    from pyswip import Prolog

    prolog=Prolog()
    prolog.assertz('comida(arroz,[hola,soy,juan],como,[pollitoxJPG,carnitaxJPG])')
    x= list(prolog.query("comida(arroz,X,A,W,R)"))
    print(x)

    '''
    s3 = boto3.resource('s3')
    file = s3.Object('progralenguajes', 'base.pl').get()['Body'].read()
    print(type(file))



pb()








