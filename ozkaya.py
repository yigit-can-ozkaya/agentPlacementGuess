from numpy import number
import pandas as pd
import numpy as np

walls="x xx  xx x"
sensors=["on","on","off","on"]

# your code starts
def get_sensor_prob(wall:bool, sensor:str):
    if wall :
        if sensor == 'on':
            return 0.7
        else:
            return 0.3
    else:
        if sensor == 'on':
            return 0.2
        else: 
            return 0.8
def get_move_prob(index: number):
    if index%2 == 0:
        return 0.8
    else:
        return 0.6
    
def wallsByIndex(index: number): 
    if index > 0:
        if walls[index-1] =='x':
            return True
    else:
        return False
    
def get_starter_array(index):
    a=[]
    for i in range(len(walls)):
        if i == index-1:
            a.append(1)
        else:
            a.append(0)
    return a


def getCalc2(agent_index):
    denemearray = get_starter_array(agent_index)
    
    multpMatrix = denemearray.copy()
    
    for moveNumber in range(1,len(sensors)+1):
        dummyArray = multpMatrix.copy()
        for index in range(agent_index-1,agent_index+moveNumber):
            if index >= len(walls):
                continue
            if index == 0:
                multpMatrix[index] = dummyArray[index]*(1-get_move_prob(index+1))*get_sensor_prob(wallsByIndex(index+1), sensors[moveNumber-1])
            elif (index == agent_index+moveNumber-1):
                multpMatrix[index]=dummyArray[index-1]*get_move_prob(index)*get_sensor_prob(wallsByIndex(index), sensors[moveNumber-2])
            elif index >= len(walls)-1 :
                multpMatrix[index] = dummyArray[index]*get_sensor_prob(wallsByIndex(index+1), sensors[moveNumber-1])
            else:
                multpMatrix[index] = dummyArray[index]*(1-get_move_prob(index+1))*get_sensor_prob(wallsByIndex(index+1), sensors[moveNumber-1])+ dummyArray[index-1]*get_move_prob(index)*get_sensor_prob(wallsByIndex(index), sensors[moveNumber-2])
                
        multpMatrix= np.array(multpMatrix)
        multpMatrix= multpMatrix/multpMatrix.sum()
        multpMatrix= multpMatrix.tolist()
        print(multpMatrix,moveNumber)
    
    return multpMatrix
        
    
    

def getCalc(agent_index, moveNumber, beforeCalc):
    if moveNumber < len(sensors)+1:
        moveForwardProb = get_move_prob(agent_index)
        notMoveProb = 1-moveForwardProb   
        sensorProb = get_sensor_prob(wallsByIndex(agent_index), sensors[moveNumber-1])
        previousProb = beforeCalc[agent_index-1]
        
        moveCalc= previousProb*moveForwardProb*sensorProb
        notMoveCalc= previousProb*notMoveProb*sensorProb
        
        afterForwardCalc = beforeCalc.copy()
        if agent_index < len(walls):
            afterForwardCalc[agent_index-1] = 0
            afterForwardCalc[agent_index] = moveCalc
        afterNotForwardCalc = beforeCalc.copy()
        afterNotForwardCalc[agent_index-1]= notMoveCalc
        
    if moveNumber == len(sensors)+1:
            beforeCalc = np.array(beforeCalc)
            return beforeCalc
    else:
        if agent_index == len(walls):
            return getCalc(agent_index,moveNumber+1,beforeCalc)
        else:
            return getCalc(agent_index+1,moveNumber+1,afterForwardCalc)+getCalc(agent_index,moveNumber+1,afterNotForwardCalc)

position_probability_for_all = np.zeros(len(walls))
probForOneIndex = 1/len(walls)

for agent_index in range(1,len(walls)+1):
    # notNormalizedResult = getCalc(agent_index,1,get_starter_array(agent_index))
    # normalizedResult = notNormalizedResult/np.linalg.norm(notNormalizedResult)
    # deneme = notNormalizedResult*1/notNormalizedResult.sum()
    # denemeCalc2 =getCalc2(agent_index)
    position_probability_for_all += getCalc2(agent_index)

robot_pos=position_probability_for_all.argmax()+1
robot_pos_prob=position_probability_for_all.max()*probForOneIndex
   
# your code ends
print('The most likely current position of the robot is',robot_pos,'with probability',robot_pos_prob)
