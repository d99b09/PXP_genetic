import random
import math
import time
import vrep
import sys

t=time.time()

def random_q(number_q):
    out_vector=[]
    for i in range(number_q):
        out_vector.append(random.uniform(-math.pi*2, math.pi*2))
    return out_vector

def random_X(number_q, num_of_select):
    out_vector = []
    for i in range(num_of_select):
        out_vector.append(random_q(number_q))
    return out_vector

def score_funct(clientID, ObjectHandles, member, T):
    joint_1=ObjectHandles[0]
    joint_2=ObjectHandles[1]
    joint_3=ObjectHandles[2]
    joint_4=ObjectHandles[3]
    point=ObjectHandles[4]
    errorCode = vrep.simxSetJointTargetPosition(clientID, joint_1, member[0], vrep.simx_opmode_oneshot_wait)
    errorCode = vrep.simxSetJointTargetPosition(clientID, joint_2, member[1], vrep.simx_opmode_oneshot_wait)
    errorCode = vrep.simxSetJointTargetPosition(clientID, joint_3, member[2], vrep.simx_opmode_oneshot_wait)
    errorCode = vrep.simxSetJointTargetPosition(clientID, joint_4, member[3], vrep.simx_opmode_oneshot_wait)
    errorCode, coord = vrep.simxGetObjectPosition(clientID, point, -1, vrep.simx_opmode_oneshot_wait)
    result = math.sqrt((coord[0] - T[0]) ** 2 + (coord[1] - T[1]) ** 2 + (coord[2] - T[2]) ** 2)
    return result

def mutate(member):


    min_q = [-2.97, -2.36, -2.36, -1.57]
    max_q = [5.93, 4.71, 4.71, 1.57]
    mutated = []
    for i in range(len(member)):
        input_vector=list(member[i])
        max_index=len(input_vector)
        mutated_index = random.choice(range(0, max_index))

        for j in range(10):
            mutation_scalar = random.uniform(0, 2) * input_vector[mutated_index]
            if ((mutation_scalar > min_q[mutated_index])and(mutation_scalar < max_q[mutated_index])):
                break
            if j == 9:
                mutation_scalar = random.uniform(min_q[mutated_index], max_q[mutated_index])

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

def select(clientID,ObjectHandles, offsprings, size, T):
    survival_value = map(lambda x: (score_funct(clientID, ObjectHandles, x, T), x), offsprings)
    select = list(map(lambda xy: xy[1], sorted(survival_value)[:size]))
    return select

def next_generation(clientID,ObjectHandles, generation, offspring_size, T):
    survival_size = len(generation)
    offsprings = []
    offsprings.append(generation[0])
    offsprings += reproduce(generation, offspring_size)
    next_generation = select(clientID,ObjectHandles, offsprings, survival_size, T)
    return next_generation

def is_approximate(clientID,ObjectHandles, generation, T):
    if (score_funct(clientID,ObjectHandles, generation[0], T))<0.01:
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

def evolution(number_q, T, num_of_select=75, num_of_offsprings = 5, max_num_generations = 30):
    clientID,ObjectHandles=getObjectHandles()
    generation = random_X(number_q, num_of_select)
    generation_index = 1
    while True:
        generation = next_generation(clientID,ObjectHandles, generation, num_of_offsprings, T)
        generation_index += 1
        if generation_index > max_num_generations:
            break
        elif is_approximate(clientID,ObjectHandles, generation, T):
            break
    q=generation[0]
    result = score_funct(clientID,ObjectHandles, q, T)    
    return q, result
