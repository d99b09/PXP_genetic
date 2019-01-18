import csv
import random
import math as m
import vrep
import sys
import time

time.process_time()

print('Program started')

vrep.simxFinish(-1)

clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

if clientID != -1:
        print("Connected to remote server")
else:
    print('Connection not successful')
    sys.exit('Could not connect')
errorCode,joint_1=vrep.simxGetObjectHandle(clientID,'PhantomXPincher_joint1',vrep.simx_opmode_oneshot_wait)
errorCode,joint_2=vrep.simxGetObjectHandle(clientID,'PhantomXPincher_joint2',vrep.simx_opmode_oneshot_wait)
errorCode,joint_3=vrep.simxGetObjectHandle(clientID,'PhantomXPincher_joint3',vrep.simx_opmode_oneshot_wait)
errorCode,joint_4=vrep.simxGetObjectHandle(clientID,'PhantomXPincher_joint4',vrep.simx_opmode_oneshot_wait)
errorCode,point=vrep.simxGetObjectHandle(clientID,'PhantomXPincher_gripperCenter_joint',vrep.simx_opmode_oneshot_wait)

FILENAME = "hemisphere_result.csv"

results = []
joints = []
r=0.25
i=random.uniform(0,360)
j=random.uniform(0,90)
fi = i*m.pi/180
alf = j*m.pi/180

x = r * m.cos(alf) * m.cos(fi)
y = r * m.cos(alf) * m.sin(fi)
z = 0.1 + r * m.sin(alf)
T = [x, y, z]

with open(FILENAME, "r", newline="") as file:
    reader = csv.reader(file)
    for row in reader:
        coord = list(map(float, row))
        results.append(((coord[0] - T[0]) ** 2 + (coord[1] - T[1]) ** 2 + (coord[2] - T[2]) ** 2)**0.5)
        joints.append([coord[3],coord[4],coord[5],coord[6]])
n=results.index(min(results))
q = joints[n]


errorCode = vrep.simxSetJointTargetPosition(clientID, joint_1, q[0], vrep.simx_opmode_oneshot_wait)
errorCode = vrep.simxSetJointTargetPosition(clientID, joint_2, q[1], vrep.simx_opmode_oneshot_wait)
errorCode = vrep.simxSetJointTargetPosition(clientID, joint_3, q[2], vrep.simx_opmode_oneshot_wait)
errorCode = vrep.simxSetJointTargetPosition(clientID, joint_4, q[3], vrep.simx_opmode_oneshot_wait)

print(results[n], q, time.process_time())
