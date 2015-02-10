import os
import csv
import json
import pprint

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, 'json')
CSV_DIR = os.path.join(BASE_DIR, 'csv')


def main():
	write_heart_csv()
	write_sleep_csv()
	write_activity_csv()

def write_heart_csv():
	filename = os.path.join(JSON_DIR, 'heart.json')
	with open(filename, 'r') as data_file:
		jsonObjects = parse_file_json_objectList(data_file)
	f = csv.writer(open('heart.csv', "wb+"))
	f.writerow(["id", "datetime", "day_value", "intra_time", "intra_value", "caloriesOut", "max", "min", "minutes", "name", "datasetInterval", "datasetType"] )
	dayIndexer = len(jsonObjects)
	for day in jsonObjects:
		for activities_heart in day['activities-heart']:
			csvIndex = dayIndexer
			csvDateTime = activities_heart['dateTime']
			csvdayValue = activities_heart['value']
			heartRateZonesListDict = activities_heart['heartRateZones']
		intra_day = day['activities-heart-intraday']
		datasetInterval = intra_day['datasetInterval']
		datasetType = intra_day['datasetType']
		for dataset in intra_day['dataset']:
			csvTime = dataset['time']
			csvintraValue = dataset['value']
			zoneDict = getZoneData(heartRateZonesListDict, csvintraValue)
			f.writerow([dayIndexer, csvDateTime, csvdayValue, csvTime, csvintraValue, zoneDict['caloriesOut'], zoneDict['max'], zoneDict['min'], zoneDict['minutes'], zoneDict['name'], datasetInterval,  datasetType]) 
		dayIndexer -= 1
	print "Finished writing heart.json"

def write_sleep_csv():
	filename = os.path.join(JSON_DIR, 'sleep.json')
	with open(filename, 'r') as data_file:
		jsonObjects = parse_file_json_objectList(data_file)
	print len(jsonObjects)
	f = csv.writer(open('sleep.csv', "wb+"))
	f.writerow(["id", "awakeCount", "awakeDuration", "awakeningsCount", "duration",
		"efficiency", "isMainSleep","logId", "dateTime", "value", "minutesAfterWakeup",
		"minutesAsleep", "minutesAwake", "minutesToFallAsleep", "restlessCount", "restlessDuration",
		"startTime", "timeInBed", "totalMinutesAsleep", "totalSleepRecords", "totalTimeInBed",]
	)
	dayIndexer = len(jsonObjects)
	for day in jsonObjects:
		totalMinutesAsleep = day['summary']['totalMinutesAsleep']
		totalSleepRecords = day['summary']['totalSleepRecords']
		totalTimeInBed = day['summary']['totalTimeInBed']
		for sleep in day["sleep"]:
			for minuteData in sleep['minuteData']:
				f.writerow([dayIndexer, sleep['awakeCount'], sleep['awakeDuration'],
					sleep['awakeningsCount'], sleep['duration'], sleep['efficiency'], 
					sleep['isMainSleep'], sleep['logId'], minuteData['dateTime'], 
					minuteData['value'], sleep['minutesAfterWakeup'], sleep['minutesAsleep'],
					sleep['minutesAwake'], sleep['minutesToFallAsleep'], sleep['restlessCount'],
					sleep['restlessDuration'], sleep['startTime'], sleep['timeInBed'], 
					totalMinutesAsleep, totalSleepRecords, totalTimeInBed,]
				)
		dayIndexer -= 1
	print "Finished writing sleep.csv"

def write_activity_csv():
	filename = os.path.join(JSON_DIR,'activity.json')
	with open(filename, 'r') as data_file:
		jsonObjects = parse_file_json_objectList(data_file)
	print len(jsonObjects)
#		jsonObjects = json.load(data_file)
	f = csv.writer(open('activity.csv', "wb+"))
	f.writerow(["id", "time", "value", "datasetInterval", "datasetType"])
	dayIndexer = len(jsonObjects)
	for day in jsonObjects:
		intraDay = day['activities-activityLevels-intraday']
		for dataset in intraDay['dataset']:
			f.writerow([dayIndexer, dataset['time'], dataset['value'],
			intraDay['datasetInterval'], intraDay['datasetType'],])
		dayIndexer -= 1
	print "finishing writing activity.csv"

# A dictionary of the heartrate zones to be comparied with intra day data
def getZoneData(dictList, value):
	for dictionary in dictList:
		if value < dictionary['max'] and value >= dictionary['min']:
			return dictionary
		
# The raw data contains several json objects in a single file.
# These objects need to parsed before we can load them and manipulate
# as a json object.
def parse_file_json_objectList(data_file):
	list_of_json_objects = []
	for line in data_file:
		while True:
			try:
				jDict = json.loads(line)
				break
			except ValueError:
				# Not yet a coplete JSON Value
				line += next(data_file)
		list_of_json_objects.append(jDict)
	return list_of_json_objects

if __name__ == "__main__":
	main()
