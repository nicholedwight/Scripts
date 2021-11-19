import json
import csv
import datetime
import os
rootdir = '<path_to_current_directory>'


def splitData():
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            path_name = os.path.join(subdir, file)
            stripped_path = path_name.split("<folder_to_split_on/>",1)[1]
            if (".csv" in stripped_path) and ("new" not in stripped_path):
                directory_name = stripped_path.split("/",1)[0]
                if not os.path.exists(f"new/{directory_name}"):
                    os.makedirs(f"new/{directory_name}")
                if not os.path.exists(f"new/{stripped_path}"):
                    with open(f'{stripped_path}', 'r') as file:
                        file_name = file.name
                        # print(file_name)
                        csv_reader = csv.reader(file, delimiter=',')
                        line_count = 0
                        splitDict = {}
                        csv_count = 0
                        splitDict['headers'] = ['Device', 'Start Date', 'Start Time', 'End Date', 'End Time', 'Value']

                        for row in csv_reader:
                            newRow = []
                            if csv_count >= 1:
                                if len(row) == 2:
                                    file.close()
                                    twoValues(file_name)
                                    return
                                if ('device' in row) and ('steps' not in row):
                                    file.close()
                                    hasHeaders(file_name)
                                    return
                                elif ('steps' in row) and ('device' not in row):
                                    file.close()
                                    hasSteps(file_name)
                                    return
                                elif ('device' in row) and ('steps' in row) and ('end_datetime'):
                                    file.close()
                                    hasHeadersStepsandEndTime(file_name)
                                    return
                                elif ('device' in row) and ('datetime' in row) and ('heartrate' in row):
                                    file.close()
                                    hasHeaders(file_name)
                                else:
                                    print('else -', file_name)
                                    file.close()
                                    twoValues(file_name)
                                    return
                            csv_count += 1

def hasHeaders(file):
    with open(f"{file}", "r") as file:
        file_name = file.name
        csv_reader = csv.reader(file, delimiter=',')
        line_count = 0
        splitDict = {}
        splitDict['headers'] = ['Device', 'Start Date', 'Start Time', 'End Date', 'End Time', 'Value']
        for row in csv_reader:
            newRow = []

            if line_count == 1:
                line_count += 1
            if line_count > 2:
                newRow.append(row[0])
                datee = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
                newRow.append(f'{datee.year}-{datee.month}-{datee.day}')
                newRow.append(f'{datee.hour}:{datee.minute}:{datee.second}')
                newRow.append("") # empty End Date
                newRow.append("") # empty End Time
                newRow.append(row[2])
                splitDict[line_count] = newRow
                line_count += 1
            
            line_count += 1
    file.close()
    writeSplitData(splitDict, file_name)

def twoValues(file):
    with open(f"{file}", "r") as file:
        file_name = file.name
        csv_reader = csv.reader(file, delimiter=',')
        line_count = 0
        if "NonFitbit" in file_name:
            device = "NonFitbit"
        else:
            device = "Fitbit"
        splitDict = {}
        splitDict['headers'] = ['Device', 'Start Date', 'Start Time', 'End Date', 'End Time', 'Value']
        for row in csv_reader:
            newRow = []
            
            newRow.append(device)
            if line_count == 1:
                line_count += 1
            if line_count > 2:
                datee = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                newRow.append(f'{datee.year}-{datee.month}-{datee.day}')
                newRow.append(f'{datee.hour}:{datee.minute}:{datee.second}')
                newRow.append("") # empty End Date
                newRow.append("") # empty End Time

                newRow.append(row[1])
                splitDict[line_count] = newRow
                line_count += 1
            
            line_count += 1
    file.close()
    writeSplitData(splitDict, file_name)

def hasSteps(file):
    with open(f"{file}", "r") as file:
        file_name = file.name
        csv_reader = csv.reader(file, delimiter=',')
        line_count = 0
        if "NonFitbit" in file_name:
            device = "NonFitbit"
        else:
            device = "Fitbit"
        splitDict = {}
        splitDict['headers'] = ['Device', 'Start Date', 'Start Time', 'End Date', 'End Time', 'Value']
        for row in csv_reader:
            newRow = []

            if line_count >= 1:
                newRow.append(device)
                for i in row[:-1]: # only first item (handle date splitting)
                    datee = datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S")
                    newRow.append(f'{datee.year}-{datee.month}-{datee.day}')
                    newRow.append(f'{datee.hour}:{datee.minute}:{datee.second}')
                    newRow.append("") # empty End Date
                    newRow.append("") # empty End Time

                    for steps in row[1:]: #only last item
                        newRow.append(steps)
                        splitDict[line_count] = newRow
            
            line_count += 1
    file.close()
    writeSplitData(splitDict, file_name)

def hasHeadersStepsandEndTime(file):
    with open(f"{file}", "r") as file:
        file_name = file.name
        csv_reader = csv.reader(file, delimiter=',')
        line_count = 0
        splitDict = {}
        splitDict['headers'] = ['Device', 'Start Date', 'Start Time', 'End Date', 'End Time', 'Value']
        for row in csv_reader:
            newRow = []

            if line_count > 1:
                newRow.append(row[0])
                datee = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
                newRow.append(f'{datee.year}-{datee.month}-{datee.day}')
                newRow.append(f'{datee.hour}:{datee.minute}:{datee.second}')
                if row[2] == " ":
                    newRow.append(row[2])
                else:
                    endDatee = datetime.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
                    newRow.append(f'{endDatee.year}-{endDatee.month}-{endDatee.day}') #  End Date
                    newRow.append(f'{endDatee.hour}:{endDatee.minute}:{endDatee.second}') #  End Time

                newRow.append(row[3])
                splitDict[line_count] = newRow
                line_count += 1
            
            line_count += 1
    file.close()
    writeSplitData(splitDict, file_name)

def writeSplitData(data, file_name):
    print('writing file - ', file_name)
    rowCount = 0
    header = []
    dataCount = 0
    finished = False
    with open(f"new/{file_name}", "w") as file:
        print(psutil.virtual_memory())
        w = csv.writer(file)
        for key, list in data.items():
            dataRow = []
            for i in list:
                if rowCount <= 6:
                    header.append(i)
                    rowCount += 1
                if rowCount == 6:
                    w.writerow(header)
                    rowCount += 1
        rowCount = 0

        data.pop('headers')
        for key, value in data.items(): # Starting on data rows
            dataRow = []
            for i in value:
                dataRow.append(i)
                rowCount += 1
                if rowCount == 6:
                    w.writerow(dataRow)
            rowCount = 0
    file.close()
    print(psutil.virtual_memory())
    splitData()


if __name__ == "__main__":
    splitData()