#This script was written for a job interview.
#The assignment was to automate the removal of all files older than a certain date.
#The files were structured in multiple layers of directories and styled as "filename-year-month-day-datatype.extension"

import sys, os, datetime

def cleanup(days_old, path):
    #Walks through all files in the path and subdirectories.
    #Calls getDate() to find file age, then calls remove() to remove files older than the days_old threshold.
    #The walkthrough is bottom-up, so files are deleted before their parent folders are. (which is the correct way of doing this.)
    now = datetime.datetime.now()
    for root, dirs, files in os.walk(path, topdown=False):
        for file_ in files:
            date = getDate(file_)
            date_diff = now - date
            if date_diff.days >= days_old:
                remove(os.path.join(root, file_))
        if not os.listdir(root):
            remove(root)
                 
def getDate(path):
    #Parses file names and creates datetime object from name string
    #This function is written for filenames formatted as "myfile-2019-08-01-data.csv".
    
    #Using "-" as a delimiter, the filename string is split into an array. 
    date_arr = path.split("-")
    month = 0
    
    #Cycle through the new array, checking to see if the substrings are decimals (i.e. part of the date)
    for d_ in date_arr:
        if str.isdecimal(d_):
            #If the substring is 4 characters long, we know it's the year and not the month or day.
            if len(d_) == 4:
                year = d_
            elif month == 0:
                month = d_
            else:
                day = d_
    try:
        #Create a datetime object with our newly identified year, month, and day strings.
        date = datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        print("Could not create date from file path %s" %path)
    return date

def remove(path):
    #Removes old files and directories
    if os.path.isdir(path):
        try:
            os.rmdir(path)
            print("Removed folder: %s" % path)
        except OSError:
            print("Unable to remove folder: %s" % path)
    else:
        try:
            if os.path.exists(path):
                os.remove(path)
                print("Removed file: %s" % path)
        except OSError:
            print("Unable to remove file: %s" % path)

cleanup(90, r'C:\MyDirectory')
    
