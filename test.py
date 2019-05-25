
import paramiko
import boto3
def x():
    import json
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('40.117.154.143',22,'dereck','Progralenguajes123')
    s3 = boto3.resource('s3')
    file = s3.Object('progralenguajes', 'base.pl').get()['Body'].read().decode().replace('\n', '')
    #entrada, salida, error=ssh.exec_command('python prolog.py' + " '" +'frijol' + "' " +'"'+file+'"')
    entrada, salida, error = ssh.exec_command('python getAll.py' + ' "' + file + '" ')
    #print('Salida:',salida.read().decode())
    x=salida.read().decode()
    #y = x[0]['Y'][0]
    print(x)
    des = json.loads(x)
    print(des[1]['IMAGES'])
    print('Error:', error.read().decode())

    ssh.close()


def pb():
    from pyswip import Prolog
    import json
    import json
    prolog=Prolog()
    prolog.assertz('comida(arroz,[hola,soy,juan],como,[estas,yo,se],[direccion1,dir2])')
    x= list(prolog.query("comida(arroz,ING,TYPE,STEPS,IMAGES)"))
    y = desAtomizar(x)
    z = json.dumps(y)
    print(z)




def desAtomizar(obj):
    size = len(obj[0]['ING'])
    cont = 0
    while (cont < size):
        cambio = str(obj[0]['ING'][cont])
        obj[0]['ING'][cont] = cambio
        cont += 1

    size = len(obj[0]['STEPS'])
    cont = 0
    while (cont < size):
        cambio = str(obj[0]['STEPS'][cont])
        obj[0]['STEPS'][cont] = cambio
        cont += 1

    size = len(obj[0]['IMAGES'])
    cont = 0
    while (cont < size):
        cambio = str(obj[0]['IMAGES'][cont])
        obj[0]['IMAGES'][cont] = cambio
        cont += 1

    return obj

x()








