import random
import math
import time
import vrep
import sys

def random_d(number_q):
    out_vector=[]
    for i in range(number_q):
        out_vector.append(random.uniform(-math.pi * 4 / 180, math.pi * 4 / 180))
    return out_vector

def random_X(number_q, num_of_select):
    out_vector = []
    for i in range(num_of_select):
        out_vector.append(random_d(number_q))
    return out_vector

def score_funct(clientID, ObjectHandles, member, T, initial_value):
    joint_1=ObjectHandles[0]
    joint_2=ObjectHandles[1]
    joint_3=ObjectHandles[2]
    joint_4=ObjectHandles[3]
    point=ObjectHandles[4]
    errorCode = vrep.simxSetJointTargetPosition(clientID, joint_1, initial_value[0]+member[0], vrep.simx_opmode_oneshot_wait)
    errorCode = vrep.simxSetJointTargetPosition(clientID, joint_2, initial_value[1]+member[1], vrep.simx_opmode_oneshot_wait)
    errorCode = vrep.simxSetJointTargetPosition(clientID, joint_3, initial_value[2]+member[2], vrep.simx_opmode_oneshot_wait)
    errorCode = vrep.simxSetJointTargetPosition(clientID, joint_4, initial_value[3]+member[3], vrep.simx_opmode_oneshot_wait)
    errorCode, coord = vrep.simxGetObjectPosition(clientID, point, -1, vrep.simx_opmode_oneshot_wait)
    result = math.sqrt((coord[0] - T[0]) ** 2 + (coord[1] - T[1]) ** 2 + (coord[2] - T[2]) ** 2)
    return result

def mutate(member):
    mutated = []
    for i in range(len(member)):
        input_vector=list(member[i])
        max_index=len(input_vector)
        mutated_index = random.choice(range(0, max_index))

        for j in range(10):
            mutation_scalar = random.uniform(0, 2) * input_vector[mutated_index]
            if ((mutation_scalar > -math.pi * 4 / 180)and(mutation_scalar < math.pi * 4 / 180)):
                break
            if j == 9:
                mutation_scalar = random.uniform(-math.pi * 4 / 180, math.pi * 4 / 180)

        output_vector = input_vector[:]
        output_vector[mutated_index] = mutation_scalar
        mutated.append(output_vector)
    return mutated

def reproduce(member, k):
    output = []
    for i in range(k):
        mut = mutate(member)
        for j in range(len(mut)):
            vec = mut[j]
            output.append(vec)
    return output

def select(clientID,ObjectHandles, offsprings, size, T, initial_value):
    survival_value = map(lambda x: (score_funct(clientID, ObjectHandles, x, T, initial_value), x), offsprings)
    select = list(map(lambda xy: xy[1], sorted(survival_value)[:size]))
    return select

def next_generation(clientID,ObjectHandles, generation, offspring_size, T, initial_value):
    survival_size = len(generation)
    offsprings = []
    offsprings.append(generation[0])
    offsprings += reproduce(generation, offspring_size)
    next_generation = select(clientID,ObjectHandles, offsprings, survival_size, T, initial_value)
    return next_generation

def is_approximate(clientID,ObjectHandles, generation, T, initial_value):
    if (score_funct(clientID,ObjectHandles, generation[0], T, initial_value))<0.01:
        return True
    else:
        return False

def getObjectHandles():


    vrep.simxFinish(-1)

    clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)


    errorCode,joint_1=vrep.simxGetObjectHandle(clientID,'PhantomXPincher_joint1',vrep.simx_opmode_oneshot_wait)
    errorCode,joint_2=vrep.simxGetObjectHandle(clientID,'PhantomXPincher_joint2',vrep.simx_opmode_oneshot_wait)
    errorCode,joint_3=vrep.simxGetObjectHandle(clientID,'PhantomXPincher_joint3',vrep.simx_opmode_oneshot_wait)
    errorCode,joint_4=vrep.simxGetObjectHandle(clientID,'PhantomXPincher_joint4',vrep.simx_opmode_oneshot_wait)
    errorCode,point=vrep.simxGetObjectHandle(clientID,'PhantomXPincher_gripperCenter_joint',vrep.simx_opmode_oneshot_wait)
    ObjectHandles=[joint_1,joint_2,joint_3,joint_4,point]
    return clientID,ObjectHandles

def d_evolution(number_q, T, initial_value, num_of_select=5, num_of_offsprings = 10, max_num_generations = 50):
    clientID,ObjectHandles=getObjectHandles()
    generation = random_X(number_q, num_of_select)
    generation_index = 1
    while True:
        generation = next_generation(clientID,ObjectHandles, generation, num_of_offsprings, T, initial_value)
        generation_index += 1
        if generation_index > max_num_generations:
            break
        elif is_approximate(clientID,ObjectHandles, generation, T, initial_value):
            break
    q=generation[0]

    value=[initial_value[0]+q[0],initial_value[1]+q[1],initial_value[2]+q[2],initial_value[3]+q[3]]

    result = score_funct(clientID,ObjectHandles, q, T, initial_value)
    #end = [value, result, generation_index]
    return value, result
