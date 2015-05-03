import socket
import select
import itertools
import time
import serial
import pypot.vrep
from pypot.vrep import from_vrep
from poppy.creatures import PoppyHumanoid


option = raw_input("Press 1 pour simulation et 2 pour vrai Poppy 2 : ")

if option=='2':
    HOST = '192.168.1.3'                 
    HOST = '127.0.0.1'
PORT = 50007              # Arbitrary non-privileged port

pypot.vrep.close_all_connections()
if option=='1':
    poppy = PoppyHumanoid(simulator='vrep') #connection à simulateur
if option=='2':
    poppy = PoppyHumanoid() # connection direct à PoppyHumanoid
print ('Connection reussi avec POPPY HUMANOID') 

poppy.compliant = False
poppy.power_up()

        # Change PID of Dynamixel MX motors
for m in filter(lambda m: hasattr(m, 'pid'), poppy.motors):
    m.pid = (1, 8, 0)  #4,2,0

for m in poppy.torso:
    m.pid = (6, 2, 0)

        # Reduce max torque to keep motor temperature low
for m in poppy.motors:
    m.torque_limit = 70

time.sleep(0.5)

### desactivation des tous les moteurs que ne seront pas utilisé
###Desactivation de la main droit
if option=='2':
    for m in poppy.r_arm:
        m.compliant = True  

    for m in poppy.head:
        m.compliant = True

    for m in poppy.legs:
        m.compliant = True

    for m in poppy.torso:
        m.compliant = True


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

print 'Waiting Connexion of Client'
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr

i=1
BLOCKSIZE = 20
lectura = ""
while i==1 :
    #Detectar desconexion del cliente
    r,w,e = select.select([conn], [], [])
  
    if r:
        t=conn.recv(1024,socket.MSG_PEEK)
        if len(t)==0:
            print 'Client Desconnected'
            print 'Waiting Connexion of Client'
            s.listen(1)#ESPERANDO NUEVA CONEXION
            conn, addr = s.accept()#aceptar nueva connexion
            print 'Connected by', addr

    while len(lectura) < BLOCKSIZE:
      data = conn.recv(BLOCKSIZE-len(lectura))
      if not data:
        break # other end is closed!
      lectura += data

    if (len(lectura)==20):
        dato1=float(lectura[0]+lectura[1]+lectura[2]+lectura[3])  # " , " 
        dato2=float(lectura[5]+lectura[6]+lectura[7]+lectura[8])  # " , " 
        dato3=float(lectura[10]+lectura[11]+lectura[12]+lectura[13])  # " , " 
        dato4=float(lectura[15]+lectura[16]+lectura[17]+lectura[18])  # " , " 
        poppy.l_shoulder_y.goal_position = dato1
        poppy.l_shoulder_x.goal_position =dato2
        poppy.l_arm_z.goal_position = dato3
        poppy.l_elbow_y.goal_position =dato4
        print (dato1)
        print (dato2)
        print (dato3)
        print (dato4)

    lectura = ""
 
    
print ('Fin')

poppy.close()  # fermé la connection avec poppy


