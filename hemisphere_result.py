import csv
import vrep
import sys

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


FILENAME = "Genetic_result.csv"
FILENAME1 = "hemisphere_result.csv"

with open(FILENAME, "r", newline="") as file:
    reader = csv.reader(file)
    for row in reader:
        q = [row[3],row[4], row[5], row[6]]
        q = list(map(float, q))
        errorCode = vrep.simxSetJointTargetPosition(clientID, joint_1, q[0], vrep.simx_opmode_oneshot_wait)
        errorCode = vrep.simxSetJointTargetPosition(clientID, joint_2, q[1], vrep.simx_opmode_oneshot_wait)
        errorCode = vrep.simxSetJointTargetPosition(clientID, joint_3, q[2], vrep.simx_opmode_oneshot_wait)
        errorCode = vrep.simxSetJointTargetPosition(clientID, joint_4, q[3], vrep.simx_opmode_oneshot_wait)
        errorCode, coord = vrep.simxGetObjectPosition(clientID, point, -1, vrep.simx_opmode_oneshot_wait)

        with open(FILENAME1, "a", newline="") as file:

            new_line = coord + q

            writer = csv.writer(file)
            writer.writerow(new_line)
