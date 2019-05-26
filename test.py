
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
    #tipos
    tipos=[]
    t='italiana'
    cont2=0
    comidi=list(prolog.query("comida(A,Y,B,W,Z)"))
    for y in prolog.query("comida(A,Y,"+t+",W,Z)"):
            n=comidi[cont2]['A']
            tipos.append(n)
            cont2+=1
    print(tipos)




    #imprime receta por nombre
    nombres=[]
    cont1=0
    n='pizza'
    for receta in prolog.query("comida("+n+",Y,B,W,Z)"):
            
            nom=comidi[cont1]['A']
            nombres.append(n)
            cont1+=1
    print(nombres)	

x('frijol')








