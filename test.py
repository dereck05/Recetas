
import paramiko
import boto3
def x():
    import json
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('40.117.154.143',22,'dereck','Progralenguajes123')
    s3 = boto3.resource('s3')
    file = s3.Object('progralenguajes', 'base.pl').get()['Body'].read().decode().replace('\n', '')
    entrada, salida, error = ssh.exec_command('python buscarTipo.py' + " '" + 'hola' + "' " + '"' + file + '"')
    #entrada, salida, error = ssh.exec_command('python getAll.py' + ' "' + file + '" ')
    #entrada, salida, error = ssh.exec_command('python buscarIng.py' + " '" + 'hola' + "' " + '"' + file + '"')
    x=salida.read().decode()
    print(x)
    #des = json.loads(x)
    #print(des)
    print('Error:', error.read().decode())

    ssh.close()


def pb():
    from pyswip import Prolog
    import json
    import json
    prolog=Prolog()
    #prolog.assertz('comida(arroz,[hola,soy,juan],como,[estas,yo,se],[direccion1,dir2])')
    prolog.assertz('ingredientes(hola,[pan,queso,leche],soy)')
    prolog.assertz('ingredientes(adios,[huevo,queso],hello)')
    prolog.assertz('ingredientes(hijos,[chile,avena,pan],wiwi)')

    prolog.assertz('obtener(ING,ACU,RES,POSA,POSB):-ingredientes(POSA,L,POSB),member(ING,L),append(ACU,L,RES)')
    #x= list(prolog.query("obtener(pan,[],R)"))
    res = []
    x = 'pan'
    for i in (prolog.query("obtener("+x+",[],RES,POSA,POSB)")):
        res.append(i)

    print(res)




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








