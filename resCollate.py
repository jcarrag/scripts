#!/usr/bin/env python
__author__ = 'james'

import csv
import datetime
import sys
import operator

def genArr():
    y = []
    for x in range(5):
        y = y + [x+1]*6
    arr = [[1, 2, 3]*10, [1, 1, 1, 2, 2, 2]*5, y]
    return arr


def readCSVFile(CSVFile):
    f = open(CSVFile, 'rb') # opens the csv file
    array = []
    reader = csv.reader(f)  # creates the reader object
    ## Read in from CSV to array
    for row in reader:   # iterates the rows of the file in orders
        if row[3] not in ('postquestionnaire', 'INSTRUCTIONS'): # Strip meta rows from data
            array.append(row) # Add row to array
    return array

def manipulateArray(array):
    ## Create condition lookup table
    y = []
    for x in range(5):
        y = y + [x+1]*6
    arr = [[1, 2, 3]*10, [1, 1, 1, 2, 2, 2]*5, y]
    sortedList = [[]]
    j = 0
    condensedList = [['Seed', 'Dynamic', 'Foregone', 'WorkerID', 'AssignmentID', 'Trial#', 'SubmitTime',
                       'Card Selection', 'Selected Value', 'Max value', 'TrialNo.', 'Condition', 'Selected Cumulative',
                       'Counter1', 'Counter2', 'Counter3', 'Counter4', 'Gender', 'Age', 'Reaction Time', 'Card1 R',
                       'Card1 Mu', 'Card2 R', 'Card2 Mu', 'Card3 R', 'Card3 Mu', 'Card4 R', 'Card4 Mu']]

    ## Make more readable
    for i in xrange(len(array)):
        split = array[i][0].split(':') # Split first column into Worker ID and Assignment ID
        array[i][0] = split[0] # Replace into array
        array[i].insert(1, split[1]) # Insert into array
        array[i][3] = datetime.datetime.fromtimestamp(int(array[i][3])/1000.0).isoformat().split('.')[0] # Convert from js timestamp to date

    ## Group by workerID
    for i in xrange(len(array)):
        if array[i][0] == array[abs(i-1)][0]: # If workerID in array == previous workerID --> add it to same sorted index
            sortedList[j].append(array[i])
        elif array[i][0] != array[abs(i-1)][0]: # Else start add to a new sorted index, update counter to start again
            sortedList.append([]) # Instantiate the next level
            sortedList[j+1].append(array[i])
            j += 1 # Update the counter (to allow the next row to be evaluated against the previous)

    ## Check each workers number of trials
    for i in xrange(len(sortedList)):
        if len(sortedList[i]) == 200: # Check to see worker has 200 trials
            condensedList.append(sortedList[i]) # If yes then copy to condensedList, headers = list[0][i]
    for j in range(1, len(condensedList)): # Start one beneath headers
        for i in xrange(len(condensedList[j])): # Go one level deeper to the trial level
            condensedList[j][i] = [9, 9, 9] + condensedList[j][i] #Place holder for condition assignment
            ## 'Right' condition: Forgone Payoff
            if arr[0][int(condensedList[j][i][11])] == 1:
                condensedList[j][i][2] = 1
            elif arr[0][int(condensedList[j][i][11])] == 2:
                condensedList[j][i][2] = 2
            elif arr[0][int(condensedList[j][i][11])] == 3:
                condensedList[j][i][2] = 3
            ## 'Middle' condition: Dynamic
            if arr[1][int(condensedList[j][i][11])] == 1:
                condensedList[j][i][1] = 1
            elif arr[1][int(condensedList[j][i][11])] == 2:
                condensedList[j][i][1] = 2
            ## 'Left' condition: Seed
            if arr[2][int(condensedList[j][i][11])] == 1:
                condensedList[j][i][0] = 1
            elif arr[2][int(condensedList[j][i][11])] == 2:
                condensedList[j][i][0] = 2
            elif arr[2][int(condensedList[j][i][11])] == 3:
                condensedList[j][i][0] = 3
            elif arr[2][int(condensedList[j][i][11])] == 4:
                condensedList[j][i][0] = 4
            elif arr[2][int(condensedList[j][i][1])] == 5:
                condensedList[j][i][0] = 5
    #print(condensedList[4])
    # for i in xrange(len(condensedList[1:])):
    #     condensedList[1:][i].sort(key = operator.itemgetter(0, 1, 2))
    return condensedList

def writeResults(list):
    if raw_input('Would you like a CSV of the results? y or n: ') == 'y':
        now = datetime.datetime.now() # Used in csv writing
        c = open('Sorted_{}.csv'.format(now.strftime("%Y-%m-%d_%H.%M")), 'wb')
        mywriter = csv.writer(c)
        for i in list:
            if len(i) < 200: # To avoid looping too deep into headers
                mywriter.writerow(i)
            else:
                for j in xrange(len(i)):
                    mywriter.writerow(i[j])
        c.close()

arr = genArr()
array = readCSVFile(sys.argv[1])
#array = readCSVFile('38.csv')
condensedList = manipulateArray(array)
writeResults(condensedList)