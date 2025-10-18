import os, argparse
import xml.etree.ElementTree as et

from tkinter.ttk import Frame, Label,Entry,Button
from tkinter import Tk, StringVar, BOTH, W, E
import readjobfile
import parse_jobfile as parse
from tkinter import messagebox

import sys

def printf(format, *args):
    sys.stdout.write(format % args)


def fprintf(fp, format, *args):
    fp.write(format % args)


# get an XML element with specified name
def getElement(parent, name):
    nodeList = []
    if parent.childNodes:
        for node in parent.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                if node.tagName == name:
                    nodeList.append(node)
    return nodeList[0]


# get value of an XML element with specified name
def getElementValue(parent, name):
    if parent.childNodes:
        for node in parent.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                if node.tagName == name:
                    if node.hasChildNodes:
                        child = node.firstChild
                        return child.nodeValue
    return None


# set value of an XML element with specified name
def setElementValue(parent, name, value):
    if parent.childNodes:
        for node in parent.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                if node.tagName == name:
                    if node.hasChildNodes:
                        child = node.firstChild
                        child.nodeValue = value
    return None

def read_tmp_file():
    filepath = parse.JobPath.tmpfile_path()

    with open(filepath, 'r') as file:
        juuid = file.readlines()

        print(f"Read  {filepath} contents {juuid} from main function")
    return juuid

class Application(Frame) :

    def __init__(self, parent, quoteuuid, price):
        # initialize frame
        Frame.__init__(self, parent)

        # set root as parent
        self.parent = parent

        print(f"Parse the Quote file and extract Quantity {quoteuuid} \n")

        try:
            xml_qu = et.parse(quoteuuid)
        except et.ParseError:
            print(f"Error in reading xml {e}")

        xml_content = xml_qu.getroot()

        #Get Attributes
        self.uuid = xml_content.attrib.get('uuid')
        self.job_uuid = xml_content.attrib.get('JobUuid')

        #Get Elements
        self.customer_drawing_uuid = xml_content.findtext('CustomerDrawingUuid')
        self.quantity = xml_content.findtext('Quantity')
        self.scale_factor_description = xml_content.findtext('ScaleFactorDescription')
        self.price = price

        # initialize UI
        self.initUI()

    def initUI(self):
        # set frame title
        self.parent.title("Request for Quote Details")

        # pack frame
        self.pack(fill=BOTH, expand=1)

        # configure grid columns
        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)
        self.columnconfigure(2, pad=3)
        self.columnconfigure(3, pad=3)
        self.columnconfigure(4, pad=3)
        self.columnconfigure(5, pad=3)

        # configure grid rows
        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)
        self.rowconfigure(6, pad=3)

        # database
        label1 = Label(self, text="Quote UUID: ")
        label1.grid(row=0, column=0, sticky=W)

        entry1 = Label(self, width=40, text=self.uuid)
        #entry1 = Entry(self, width=40, textvariable=self.uuid)
        entry1.grid(row=0, column=1)

        # bench mark
        label2 = Label(self, text="Job UUID : ")
        label2.grid(row=0, column=2, sticky=W)

        entry2 = Label(self,
                       width=40,
                       text=self.job_uuid)
             #entry2 = Entry(self, width=30, textvariable=self.job_uuid)
        entry2.grid(row=0, column=3, sticky=W)

        # Drawing UUID
        label4 = Label(self, text="Drawing : ")
        label4.grid(row=1, column=0, sticky=W)

        entry4 = Label(self, width=40, text=self.customer_drawing_uuid)
        #entry4 = Entry(self, width=30, textvariable=self.customer_drawing_uuid)
        entry4.grid(row=1, column=1)

        # Quantity
        label5 = Label(self, text="Quantity : ")
        label5.grid(row=1, column=2, sticky=W)

        self.quantity_str: str = self.quantity
        entry5 = Label(self, width=23, text=self.quantity_str)
        #entry5 = Entry(self, width=30, textvariable=self.quantity)
        entry5.grid(row=1, column=3)

        # Price
        label5 = Label(self, text="Price : ")
        label5.grid(row=1, column=4, sticky=W)

        entry5 = Label(self, width=23, text=self.price)
        #entry5 = Entry(self, width=30, textvariable=self.quantity)
        entry5.grid(row=1, column=5)

        # blank line
        label6 = Label(self, text="")
        label6.grid(row=2, column=3, sticky=E + W)

        # create OK button
        #button1 = Button(self, text="OK", command=self.onOK)
        #button1.grid(row=3, column=0, sticky=E)

        # create Cancel button
        #button2 = Button(self, text="Cancel", command=self.onCancel)
        #button2.grid(row=3, column=1, sticky=E)

    def onOK(self):
        # set values in xml document
        setElementValue(self.quoteuuid, "Quote", self.uuid.get())
        setElementValue(self.xmlDocument, "Job", self.job_uuid.get())
        setElementValue(self.xmlService, "Drawing", self.customer_drawing_uuid.get())
        setElementValue(self.xmlService, "Quantity", self.quantity.get())
        setElementValue(self.xmlService, "Scale", self.scale_factor_description.get())

        # open XML file
        #jobfile
        f = open(jobfile, "w")

        # set xml header
        fprintf(f, '<?xml version="1.0" encoding="utf-8"?>\n')

        # write XML document to XML file
        self.quoteuuid.writexml(f)

        # close XML file
        f.close()

        # show confirmation message
        tkMessageBox.showerror("Message", "Configuration updated successfully")

        # exit program
        self.quit();

    def onCancel(self):
        # exit program
        self.quit();


def main():
    # initialize root object
    root = Tk()

    # set size of frame for initUI_new
    root.geometry("710x270+300+300")

    #Call Application for multiple Quote files
    j_file = ''.join(str(x) for x in read_tmp_file())
    j_path: str = parse.JobPath.rootpath

    print(f"\n\nBASHOBI Print that argument has been passed {j_file}")

    #Path to the Job file
    ffp=os.path.abspath(j_file)

    can_parse=parse.VarType.FALSE
    for base, dirs, files in os.walk(j_path):
        for name in files:
    #        print(f"Path to the job file is {j_path} for file {name}")
            if name == j_file + '.xml' and name[:3] == "JOB":
                j_f = j_file + '.xml'
                j_path =  base
                print(f"{j_file}  --> {j_path}")
                parse_tmp_file = os.path.abspath(os.path.join(base, name))
                can_parse=parse.VarType.TRUE
                #(f"Rest here {type(can_parse)} as {can_parse}  {j_file}   ,  {parse_tmp_file}")

                break
            else:
                can_parse=parse.VarType.FALSE
                #messagebox.showinfo("Message", "Nothing to parse as file is not the xml.")
        # Found the in focus Job File , so break out of the loops
        # and begin analysing corresponding TXfiles
        if can_parse:
            break

    if can_parse:
        print(f"Evaluated as True  here {j_file}   ,  {j_path}")

    #Call read_jobs() with JobUUID
        reqfile_xml, qfile_xml = readjobfile.read_jobs(j_file, j_path)
        #reqfile_xml, qfile_xml = readjobfile.read_jobs(j_file)
        print(f"List of Req files in Job --> {reqfile_xml}")
        print(f"List of Quote files in Job --> {qfile_xml}")

    #Construct filenames
        qfile_list = ""
        for qfile in qfile_xml.split(','):
            qfile_list =  "TX-" + qfile +".xml" + "," + qfile_list

        for reqfile in reqfile_xml.split(','):
            print(f"UUID of Request from Job file {reqfile}")
            f_req = "TX-" + reqfile +".xml"
            #print(f"Constructed file name {f_req} and {j_path}\n")
            f_req = os.path.join(j_path, f_req)

            print(f"Constructed Request file name {f_req} \n")

            #Extract price from Quote xml file
            #Loop through each quote file to match the Request UUID
            price = readjobfile.pair_req_to_quote(reqfile, j_path, qfile_list)
            #print(f" Matched Quote file Price extracted {price}")

        #Call App for each request
            app = Application(root, f_req, price)


    # enter main loop . Uncomment this to test standalone.
    #root.mainloop()

def demo_qty_and_price(is_file_name):
    if is_file_name and is_file_name != "ignore":
        print(f" Module called with a specific file {is_file_name}")
    else:
        print("Blanket summary")
    main()

# if this is the main thread then call main() function
if __name__ == '__main__':
    main()