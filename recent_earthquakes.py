# Below code prints earthquake stats to txt file in same folder
# Example file for parsing and processing JSON
# Adapted from Ch. 4 and Ch. 5 of 
# https://www.linkedin.com/learning/learning-python-2/

import urllib.request # instead of urllib2 like in Python 2.7
import json
import datetime # import to get current system timestamp on file name

# Need to import below to ignore certificates in Python3 updates
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def printResults(data):
  # Use the json module to load the string data into a dictionary
  theJSON = json.loads(data)

  # Creating file write and append objects to print to
  timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
  filename = "Recent_Major_Earthquakes_" + timestamp + ".txt"
  fo = open(filename, 'w') 
  fa = open(filename, 'a') 
  
  # now we can access the contents of the JSON like any other Python object
  if "title" in theJSON["metadata"]:
    print (theJSON["metadata"]["title"], file = fo) # appending fo or fa to print to txt file
  
  # output the number of events, plus the magnitude and each event name  
  count = theJSON["metadata"]["count"];
  print (str(count) + " events recorded", file = fa)
  
  # for each event, print the place where it occurred
  for i in theJSON["features"]:
    print (i["properties"]["place"], file = fa)
  print ("--------------\n", file = fa)

  # print the events that only have a magnitude greater than 4
  print ("\n\nEvents that were 4.0 or greater in magnitude:", file = fa)
  for i in theJSON["features"]:
    if i["properties"]["mag"] >= 4.0:
      print ("%2.1f" % i["properties"]["mag"], i["properties"]["place"], file = fa)
  print ("--------------\n", file = fa)

  # print only the events where at least 1 person reported feeling something
  print ("\n\nEvents that were felt:", file = fa)
  for i in theJSON["features"]:
    feltReports = i["properties"]["felt"]
    if (feltReports != None):
      if (feltReports > 0):
        print ("%2.1f" % i["properties"]["mag"], i["properties"]["place"], " reported " + str(feltReports) + " times", file = fa)
  
  
def main():
  # define a variable to hold the source URL
  # In this case we'll use the free data feed from the USGS
  # This feed lists all earthquakes for the last day larger than Mag 2.5
  urlData = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"
  
  # Open the URL and read the data
  webUrl = urllib.request.urlopen(urlData)
  print ("result code: " + str(webUrl.getcode()))
  if (webUrl.getcode() == 200):
    data = webUrl.read()
    # print out our customized results
    printResults(data)
  else:
    print ("Received an error from server, cannot retrieve results " + str(webUrl.getcode()))

if __name__ == "__main__":
  main()
