### Intro

Nessus creates a native file called nessus.db file when generating scan reports.

If used in the default root installed nessus RPM on Linux, with admin running scans these are located in:

```/opt/nessus/var/nessus/users/admin/reports```

These scan reports are manually downloadable from the Nessus GUI and are also exposed by the Nessus REST API.   

This ```py-nessus-wrapper``` makes use of [metaevolution/py-nessus](https://github.com/metaevolution/py-nessus)

### Use case

One use case:

The reason why this wrapper was created is because we needed to expose nessus report data in an xml format consumable by Splunk.

Splunk currently makes available a python based "TA" which takes Nessus XML data as an input, and then consumes the output data in a "batch" fashion.  This preserves the original XML data.

The <b>Dependency</b> for this script is that the data be in XML format.

### script options

    # Arg[1]: Specify the URL of the Nessus Server with port (api access)
    # Arg[2]: Specify the user of the Nessus Server (which user the reports are stored as)
    # Arg[3]: Specify the password for the user to the Nessus Server 
    # Arg[4]: Specify the folder for the downloaded nessus log files
    # Arg[5]: Specify the folder to verify and prevents duplicate downloads of Nessus logs


Note: Storing the password for a nessus server in a script is not necessarily good practice.   We do not recommend doing this in an environment where you do not have compensating controls in place.

### Usage Example

Nessus is installed in /opt/nessus as root.

Splunk Enterprise (not agent) is installed in /opt/splunk as splunk:splunk

Data directory is created as /data/nessus/in  /data/nessus/out and /data/nessus/external-scripts

git clone git@github.com:metaevolution/py-nessus.git into ```external-scripts```

git clone git@github.com:djfang/py-nessus-wrapper.git

The scripts must run as ROOT in order to access nessus.  The data must reside as splunk:splunk in order for splunk to access the data.  The wrapper handles this withing the confines of the directory structure above.


