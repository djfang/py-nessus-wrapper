# Script to Download Nessus Formatted XML via Nessus API
# Dependent: https://github.com/metaevolution/py-nessus

from nessus import api
import util
import pprint
import sys
import os

# Used for Chowning Files to Splunk User and Group
import pwd
import grp


##### Usage Information #### 
# Syntax: getXMLNessus.py <Nessus URL> <Nessus User> <Nessus Password> <Output Directory> <Verify Directory>
############################

# Obtain Splunk UID / GID
splunkUID = pwd.getpwnam("splunk").pw_uid
splunkGID = grp.getgrnam("splunk").gr_gid

# Nessus Constants
NESSUS_STATUS_COMPLETED = "completed"
NESSUS_EXTENSION = "xml.nessus"

# Specifies the Fixed Number of Arguments Read of Command Line
SCRIPT_FIXED_ARGUMENTS = 6

# Reads the Command Line Arguments into Array
getCMDArguments = sys.argv

# Total Number of Arguments
totalCMDArguments = len(sys.argv)

if (totalCMDArguments == SCRIPT_FIXED_ARGUMENTS):

    # Arg[1]: Specify the URL of the Nessus Server with port
    # Arg[2]: Specify the user of the Nessus Server
    # Arg[3]: Specify the password for the user to the Nessus Server
    # Arg[4]: Specify the folder for the downloaded nessus log files
    # Arg[5]: Specify the folder to verify and prevents duplicate downloads of Nessus logs
    nessusURL = sys.argv[1]
    nessusUser = sys.argv[2]
    nessusPassword = sys.argv[3]
    nessusFileOutputFolder = sys.argv[4]
    nessusFileVerifyFolder = sys.argv[5]

    # Create an Instance of the API
    a = api.Api()
    a.login(nessusURL, nessusUser, nessusPassword)

    # Iterate through all reports on Nessus and download only the "completed" reports
    for report in a.report_list()['reports']['report']:

        reportName = report['name']
        reportStatus = report['status']
        print "Report Name: " + reportName
        print "Report Status: " + reportStatus

        tempFileName = nessusFileOutputFolder + "/" + report['name'] + "." + NESSUS_EXTENSION
        verifyFileName = nessusFileVerifyFolder + "/" + report['name'] + "." + NESSUS_EXTENSION

        if (os.path.isfile(verifyFileName)):
            print "    File Already Exists, skipping..."
        
        else:
            if (reportStatus == NESSUS_STATUS_COMPLETED):
                print "    Downloading report..."
                downloadReport = a.file_report_download(report['name'])
        
                print "Open File for Writing..."
                f = open(tempFileName, 'w')
        
                print "Writing Report to File..."
                f.write(downloadReport)
        
                print "Report Writing Completed and updating file permissions"

                # Chowning File to Splunk User and Group
                os.chown(tempFileName, splunkUID, splunkGID)

                print "Done... \n"

else:
    print "Please check your arguments. Received " + totalCMDArguments \
        + " arguments, requires: " + SCRIPT_FIXED_ARGUMENTS \
        + " \n Syntax: getXMLNessus.py <Nessus URL> <Nessus User> <Nessus Password> <Output Directory> <Verify Directory>"

