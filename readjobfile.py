
import re
import os
import xml.etree.ElementTree as Et
import parse_jobfile
from parse_jobfile import JobPath

# Read the file
#files={"JOB_txt.xml"}
#files={"JOB-78649DF4-3EA0-89C3-C4A7-CCC2DB69F290.xml"}
#filepath= "C:\\Users\\Bashobi\\PycharmProjects\\PythonProject\\GasketUI\\Jobs\\Day_1"

def extract_from_job(is_job_name):
    print(f"The Directory is --> {os.path.dirname(is_job_name)}")
    print(f"The File is --> {os.path.basename(is_job_name)}")
    with open(is_job_name, 'r') as file:
        lines = file.readlines()

def read_jobs(is_job_name: str, filepath: str):
   # is_job_name="Test"
    #if is_job_name:
    #    files=is_job_name+".xml"
    #    print(f"File selected : {files}")

    #for qfile in files:
    #    print(f"File selected : {qfile}")
    #    jobfile = os.path.join(filepath, qfile)

    # Convert the list data type of passed argument to a string
    jobfile = ''.join(str(x) for x in is_job_name)
   # Associate path to the string which is the JOB file
    jobfile = os.path.join(filepath,jobfile+ '.xml')
    print(f"Fill JOb file {jobfile}")
# THis section is to read JOB as an xml
    try:
        xml_qu = Et.parse(jobfile)
    except Et.ParseError:
        print(f"Error in reading xml {e}")

    xml_content = xml_qu.getroot()

# Get Attributes
    topattr = xml_content.find('pais')
    qlist = ""
    reqlist = ""

    for l1 in topattr.findall('l1'):
        text = l1.text
        timestamp, uuid, filetag = text.split(',')
        print(f"Timestamp {timestamp}  uuid {uuid}   filetag {filetag}")
        if filetag == "Quote":
            qlist = uuid + ',' + qlist
        if filetag == "RequestForQuote":
            reqlist = uuid + ',' + reqlist
    print(f" Lists prepared Q  as {qlist}")
    print(f" Lists prepared Req  as {reqlist}")
   # End reading JOB as xml

    #print(f"ARg to be opened {jobfile}")
    ## Read the JOB file
    #with open(jobfile, 'r') as file:
    #    lines = file.readlines()

    ## Use regex to filter lines containing 'Quote'
    #pattern = re.compile(r'^(.*?),(.*?),Quote$')
    #matches = [pattern.match(line.strip()) for line in lines]
    ##print(matches)
    #filtered_data = [m.groups() for m in matches if m]
    ## Print the result
    #qlist = ""

    #for row in filtered_data:
    #    print(row[1])
    #    qlist = row[1] + ',' + qlist

    ## Use regex to filter lines containing 'RequestForQuote'
    #pattern = re.compile(r'^(.*?),(.*?),RequestForQuote$')
    #matches = [pattern.match(line.strip()) for line in lines]
    ##print(matches)
    #filtered_data = [m.groups() for m in matches if m]
    ##print(filtered_data)

    ## Print the result
    #reqlist = ""

    #for row in filtered_data:
    #    print(row[1])
    #    reqlist = row[1] + ',' +  reqlist
    ##Return lists of UUIDs of Quote and UUIDs of RequestforQuote from JOB.xml
    return reqlist.rstrip(',') , qlist.rstrip(',')

#Match the RequestforQuote file with its corresponding Quote file
#Extract Quantity from one file and Price from the other file
def pair_req_to_quote(req_uuid, j_path, qfile_list):

    #Strip rightmost comma
    qfile_list = qfile_list.rstrip(',')
    #Loop through each quote file
    for f_quote in qfile_list.split(','):
        print(f" List of quote files {qfile_list}")
        print(f"Inside Pair function step 1-- {f_quote}")
        #filepath = JobPath.filepath
        print(f"Inside pair function step 2-- {j_path}")
         # Read the file
        f = os.path.join(j_path, f_quote)
        #f = os.path.join(parse_jobfile.JobPath.filepath, f_quote)
        print(f"Inside pair function step 3-- {f}")
        #Is the QUote file xml readable?
        try:
            xml_qu = Et.parse(f)
        except Et.ParseError:
            print(f"Error in reading xml {e}")

        xml_content = xml_qu.getroot()

        # Get Attributes
        # This is the line in the xml that has the tag 'Quote'
        quote = xml_content.attrib.get('uuid')

         # Get Elements
        RequestForQuoteUuid = xml_content.findtext('RequestForQuoteUuid')
        Price = xml_content.findtext('Price')
        print(f" Extraction of elements such as {RequestForQuoteUuid} to match with {req_uuid}")
        if RequestForQuoteUuid == req_uuid:
            print(f"Matches {RequestForQuoteUuid} with {req_uuid} and price is {Price}")
            return Price



#read_jobs()

