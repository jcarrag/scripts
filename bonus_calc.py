#!/usr/bin/env python
__author__ = 'james'

import csv     # imports the csv module
import sys      # imports the sys module
import datetime
import operator


def readCSVFile(CSVFile=sys.argv[1]):
    f = open(CSVFile, 'rb') # opens the csv file
    array = []
    finalList = []
    reader = csv.reader(f)  # creates the reader object

    for row in reader:   # iterates the rows of the file in orders
        if row[3] not in ('postquestionnaire', 'INSTRUCTIONS'): # Strip meta rows from data
            array.append(row) # Add row to array
    ## Cleaning up
    for i in xrange(len(array)):
        split = array[i][0].split(':') # Split first column into Worker ID and Assignment ID
        array[i][0] = split[0] # Replace into array
        array[i].insert(1, split[1]) # Insert into array
        array[i][3] = datetime.datetime.fromtimestamp(int(array[i][3])/1000.0).isoformat().split('.')[0] # Convert from js timestamp to date
        ## Only use last entry for each workerID
        #if array[i][0] != array[abs(i-1)][0]: # abs() so don't allow negative indexing (for first line)
        if array[i][0] != array[abs(i-1)][0] and int(array[abs(i-1)][2]) == 200: # Must have completed 200 trials
            finalList.append(array[i-1])
        #elif i == len(array) == 200: # Append last line
        elif i == len(array) and int(array[abs(i-1)][2]) == 200: # Append last line, must have completed 200 trials
            finalList.append(array[i])
    finalList.sort(key=operator.itemgetter(3)) # Sort finalList by date
    f.close()      # Close CSV file
    return finalList


def printResults(list):
    totalBonus = 0
    for i in xrange(len(list)):
        print "{}. ID: {}, AssID: {}, Trials: {}, Score: {}, Bonus: ${}, Date: {}".format(i+1, list[i][0], list[i][1], list[i][7], list[i][9], round(float(list[i][9])/30000, 2), list[i][3])
        totalBonus = totalBonus + round(float(list[i][9])/15000, 2)
    #print "Average Score: {}, Bonus: Total: {}, Average: {}".format(list[i][9], totalBonus, totalBonus/len(list)) # No longer relevant (changed payment scheme)


def writeResults(list):
    now = datetime.datetime.now() # Used in csv writing
    if raw_input('Would you like a CSV of the results? y or n: ') == 'y':
        c = open('{}.csv'.format(now.strftime("%Y-%m-%d_%H.%M")), 'wb')
        mywriter = csv.writer(c)
        for row in list:
            mywriter.writerow(row)
        c.close()


finalList = readCSVFile()
printResults(finalList)
writeResults(finalList)