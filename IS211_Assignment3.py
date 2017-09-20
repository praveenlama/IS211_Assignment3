# Praveen Lama
# IS 211
# Assignment 3
# Fall 2017


import argparse
import logging
import urllib2
import csv
import datetime
import operator
import re


# function to return the file from url
def downloadData(url):
    file = urllib2.urlopen(url)
    return file


# function to process the data from csv file and prints the result
def processData(data):
    data = csv.reader(data)
    dateFormat = "%Y-%m-%d %H:%M:%S"
    totalHits = 0
    imgHits = 0
    safari = chrome = firefox = msie = 0 # Users Agents

    hours = {i: 0 for i in range(0, 24)}

    for i in data:
        result = {"path": i[0], "date": i[1], "browser": i[2], "status": i[3], "size": i[4]}

        date = datetime.datetime.strptime(result["date"], dateFormat)
        hours[date.hour] = hours[date.hour] + 1

        totalHits += 1

        if re.search(r"\.(?:jpg|jpeg|png|gif)$", result["path"], re.I | re.M):
            imgHits += 1

        elif re.search("chrome/\d+", result["browser"], re.I):
            chrome += 1

        elif re.search("safari", result["browser"], re.I) and not re.search("chrome/\d+", result["browser"], re.I):
            safari += 1

        elif re.search("firefox", result["browser"], re.I):
            firefox += 1

        elif re.search("msie", result["browser"], re.I):
            msie += 1

    imageRequest = (float(imgHits) / totalHits) * 100
    browsers = {"Safari": safari, "Chrome": chrome, "Firefox": firefox, "MSIE": msie}

    print "Finished with processing.\n"
    print "Results Analysis"
    print "Total Number of Hits (all browser) : %s" % totalHits
    print "Image requests account for {0:0.1f}% of all requests.".format(imageRequest)
    print "Most Popular Browser : %s" % (max(browsers.iteritems(), key=operator.itemgetter(1))[0]) + "\n"

    sortedTimes = sorted(hours.items(), key=operator.itemgetter(1))
    sortedTimes.reverse() # we need descending order

    for i in sortedTimes:
        print "Hour %02d has %s hits." % (i[0], i[1])


# to simulate a loader
def loadingSimulator():
    print "Started Processing ..."
    for i in range(1, 7):
        for j in range(1,i):
            print ".",
        print "\n"

def main():
    # main function, the parser will parse the --url argument from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Enter URL to fetch a csv file")
    args = parser.parse_args()

    # if url argument is passed
    if args.url:
        try:
            data = downloadData(args.url)
            loadingSimulator(); # just for little UI work
            processData(data)
        except urllib2.URLError as e:
            print "Invalid URL"
            logging.info('Invalid URL');
    else:
        print "Please run the program with an url Argument. Example python test.py --url urlpath"


if __name__ == "__main__":
    main()