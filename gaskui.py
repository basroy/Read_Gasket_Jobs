from tkinter import *
import parse_jobfile as parse
from tkcalendar import DateEntry
from tkinter import ttk
import os, webbrowser
import subprocess
import platform
import readQuotefile
import datetime as dt
import xml.etree.ElementTree as ET
from tkinter import filedialog
from tkinter import messagebox


opt1: str = 'View Quantity on all Job Quotes'
opt2: str = 'View Quantity and Price on all Job Quotes'
opt3: str = 'View Quantity on final Job Quote'
opt4: str = 'View Quantity and Price on final Job Quote'

#path_to_my_project = 'C:\\Users\\Bashobi\\PycharmProjects\\PythonProject\\GasketUI\\Jobs'
path_to_my_project = parse.JobPath.rootpath

"""
def convert_job_xml_to_txt(startnode):
    for f_job in os.listdir(startnode):
        full_path = os.path.join(startnode, f_job)

        if os.path.isdir(full_path):
            convert_job_xml_to_txt(full_path)  # Recurse
            continue

        if f_job.startswith("JOB") and f_job.endswith(".xml"):
            try:
                tree = ET.parse(full_path)
                root = tree.getroot()
                pais = root.find('pais')
                if pais is None:
                    print(f"No <pais> section found in {f_job}")
                    continue

                lines = []
                for l1 in pais.findall('l1'):
                    if l1.text:
                        clean_line = l1.text.strip()
                        lines.append(clean_line)

                if lines:
                    txt_filename = f_job.replace(".xml", ".txt")
                    txt_path = os.path.join(startnode, txt_filename)
                    with open(txt_path, "w") as txtfile:
                        txtfile.write('\n'.join(lines))
                    print(f"Converted {f_job} to {txt_filename}")
                else:
                    print(f"No valid <l1> entries in {f_job}")

            except ET.ParseError as e:
                print(f"Parse error in {f_job}: {e}")
"""
class GaskUI:
    def __init__(self, job):
        self.job = job
        self.job.title('File Preview Window')
        self.job.geometry('900x1000+1+1')
        self.job.resizable(10, 10)
        #self.job.config(bg='grey')
        self.job.config(bg=parse.Colors.GRAY)
        self.titleImage = PhotoImage(file="images/filingicon.png")
        jobLabel = Label(self.job,
                         image=self.titleImage,
                         compound=LEFT,
                         text='Preview Daily Job Quotes',
                         font=('serif', 14, 'bold'),
                         fg=parse.Colors.WHITE,
                         bg=parse.Colors.GREEN,
                         anchor='w',
                         padx=20,
                         )
        jobLabel.place(x=40, y=10, relwidth=1)

        updJOBButton = Button(self.job,
                              text='JOB to XML',
                              font=('serif', 10, 'bold'),
                              fg=parse.Colors.WHITE,  # 'white',
                              bg=parse.Colors.CYAN,  # '#018c48',
                              anchor='w',
                              padx=20,
                              command=lambda: fix_Jobfile(parse.JobPath.rootpath)
                              )
        updJOBButton.place(x=540, y=10, width=120)

        updJOBButtonTXT = Button(self.job,
                                 text='JOB to TXT',
                                 font=('serif', 10, 'bold'),
                                 fg=parse.Colors.WHITE,
                                 bg=parse.Colors.CYAN,
                                 anchor='w',
                                 padx=20,
                                 command=lambda: convert_job_xml_to_txt(parse.JobPath.rootpath)
                                 )
        updJOBButtonTXT.place(x=540, y=50, width=120)

        def browse_for_job_folder():
            selected_path = filedialog.askdirectory()
            if selected_path:
                parse.JobPath.rootpath = selected_path
                print(f"New job folder selected: {selected_path}")
                # Optional: refresh the TreeView here

        browseButton = Button(self.job,
                              text="Browse Job Folder",
                              font=('serif', 10, 'bold'),
                              fg=parse.Colors.WHITE,
                              bg=parse.Colors.CYAN,
                              anchor='w',
                              padx=20,
                              command=browse_for_job_folder)
        browseButton.place(x=680, y=50, width=160)

        date = dt.datetime.now()
        subtitleLabel = Label(self.job,
                              #text='Welcome Glenn\t\tDate: 04-06-2025 \t\t Time: 12:20:00 pm',
                              text=f"Welcome Glenn        {date:%A, %B %d, %Y  ::  %H:%M}",
                              font=('serif', 14),
                              fg=parse.Colors.WHITE,
                              bg=parse.Colors.GREEN
                              )
        subtitleLabel.place(x=40, y=100, relwidth=1)
        # cal=DateEntry(job,
        #              selectmode='day',
        ##              font=('arial', 13),
        #              fg='white',
        #              bg='#018c48'
        #              )
        # cal.place(x=70,y=110,relwidth=1)

        leftFrame = Frame(self.job
                          )
        leftFrame.place(x=0, y=130, width=222, height=555)

        self.leftImage = PhotoImage(file="images/warehouse.png")
        l_panelLabel = Label(leftFrame,
                             image=self.leftImage)
        # leftImageLabel.grid(row=0,column=0)
        l_panelLabel.pack()

        menuLabel = Label(
            leftFrame,
            text='Menu',
            font=('serif', 14),
            bg=parse.Colors.GREENMATT  # '#009688'
        )
        menuLabel.pack(fill="x")

        def validate_and_open_jobs():
            rootpath = parse.JobPath.rootpath
            if not rootpath or not os.path.isdir(rootpath) or not os.listdir(rootpath):
                messagebox.showerror(
                    "Invalid Job Folder",
                    "⚠️ Please select a valid job folder before continuing."
                )
                return
            job_list()

        self.coffee = PhotoImage(file="images/coffee_hot.png")
        jobs_button = Button(leftFrame,
                             text='Jobs',
                             font=('serif', 13),
                             image=self.coffee,
                             compound=LEFT,
                             padx=15,
                             cursor='circle',
                             bg=parse.Colors.GREENMATT,  # '#009688',
                             command=validate_and_open_jobs
                             )
        jobs_button.pack(fill="x")
        # jobs_button.configure(command=job_list())



        quotes_button = Button(leftFrame,
                               text='Quotes',
                               font=('serif', 13),
                               bg=parse.Colors.GREENMATT,  # '#009688'
                               )
        quotes_button.pack(fill="x")

        orders_button = Button(leftFrame,
                               text='Orders',
                               font=('serif', 13),
                               bg=parse.Colors.GREENMATT,  # '#009688'
                               )
        orders_button.pack(fill="x")

        job_frame = Frame(self.job,
                          bg=parse.Colors.CYAN,  # '#2C3550',
                          bd=3,
                          relief=RIDGE
                          )
        job_frame.place(x=300, y=180, height=110, width=170)
        total_job_label = Label(job_frame,
                                text='Total Jobs',
                                bg=parse.Colors.CYAN,  # '#2C3E50',
                                fg='white',
                                font=('serif', 15))
        total_job_label.pack()
        total_job_count_label = Label(job_frame,
                                      text='0',
                                      bg=parse.Colors.CYAN,  # ,
                                      fg='white',
                                      font=('arial', 15))
        total_job_count_label.pack()

        quote_frame = Frame(job,
                            bg=parse.Colors.BLUE,  # '#2C3550',
                            bd=3,
                            relief=RIDGE
                            )
        quote_frame.place(x=600, y=180, height=110, width=170)
        total_quotes_label = Label(quote_frame,
                                   text='Total Quotes',
                                   bg=parse.Colors.BLUE,  # '#2C3E50',
                                   fg='white',
                                   font=('arial', 15))
        total_quotes_label.pack()
        total_quotes_count_label = Label(quote_frame,
                                         text='0',
                                         bg=parse.Colors.BLUE,  # '#2C3E50',
                                         fg='white',
                                         font=('arial', 15))
        total_quotes_count_label.pack()

        order_frame = Frame(self.job,
                            bg=parse.Colors.CYAN,  # '#2C3550',
                            bd=3,
                            relief=RIDGE
                            )
        order_frame.place(x=300, y=380, height=110, width=170)

        total_orders_label = Label(order_frame,
                                   text='Total Orders',
                                   bg=parse.Colors.CYAN,  # '#2C3E50',
                                   fg='white',
                                   font=('arial', 15))
        total_orders_label.pack()
        total_orders_count_label = Label(order_frame,
                                         text='0',
                                         bg=parse.Colors.CYAN,  # '#2C3E50',
                                         fg='white',
                                         font=('arial', 15))
        total_orders_count_label.pack()


class FileApp(Frame):
    def __init__(self, master, path=None, **kwargs):
        #Frame.__init__(self, master)
        super().__init__(master, **kwargs)
        self.tree = ttk.Treeview(self, show='tree')
        self.tree.pack(side='left', fill='both', expand=True)

        ysb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
        self.tree.heading('#0', text=path, anchor='w')

        # Set initial column width and allow it to stretch
        self.tree.column('#0', width=400, stretch=True)
        self.tree.rowconfigure(0,minsize=310,weight=2)

        abspath = os.path.abspath(path)
        root_node = self.tree.insert('', 'end', text=abspath, open=True)
        #self.process_directory(root_node, abspath, visited=set(), depth=0, max_depth=5)
        self.process_directory(root_node, abspath)


        # Without this line, horizontal scrolling doesn't work properly.
        self.tree.column('#0', width=400, stretch=True)
        self.tree.rowconfigure(0,minsize=310,weight=2)

        self.tree.grid(row=0, column=0)
        ysb.grid(row=0, column=1, sticky='ns')
        xsb.grid(row=1, column=0, sticky='ew')
        self.grid()
        start_path = "."  # Starting folder (current directory)
        #self.insert_items('', start_path)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    # When the focus is on a file in the file viewer, copy the UUID portion of the
    # file if it is the JOB file into file 'tmp_file'
    def Copy_Jobname(self,file_path):
        #Input parameter is the JOB file name highlighted in the treeview
        #
        f=os.path.basename(file_path)  #Extract path
        #p=os.path.dirname(file_path)   #Extract Job file name
        p=parse.JobPath.rootpath
        juuid=f.split('.') # Separate filename from extension
        tmpf=os.path.join(p,'tmp_file') #Temporary file in same location

        print(f" Write {juuid[0]}  into file {tmpf}")
        f_job = juuid[0]
        if f_job[:3] == "JOB":
            with open(tmpf,"w") as file:
                print(f" Write {juuid[0]}  into file {tmpf}")
                readQuotefile.fprintf(file, juuid[0])
            file.close()

    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
#            oid = self.tree.insert(parent, 'end', text=p, open=False)
            oid = self.tree.insert(parent, 'end', text=p, open=False, values=[abspath])

            if isdir:
               self.process_directory(oid, abspath)

    '''
    def process_directory(self, parent, path, visited, depth=0, max_depth=5):
        if depth > max_depth:
            return

        try:
            real_path = os.path.realpath(path)
            if real_path in visited:
                return
            visited.add(real_path)

            entries = os.listdir(path)
        except Exception:
            return

        for entry in entries:
            if entry.startswith('.'):
                continue

            abspath = os.path.join(path, entry)
            isdir = os.path.isdir(abspath)

            try:
                oid = self.tree.insert(parent, 'end', text=entry, open=False, values=[abspath])
            except Exception:
                continue

            if isdir:
                self.process_directory(oid, abspath, visited, depth + 1, max_depth)
        '''
    def open_file(self,file_path):
        if platform.system() == "Windows":
            #try:
                webbrowser.open(file_path)
                self.Copy_Jobname(file_path)

                #os.startfile(file_path)
            #except ReferenceError

        elif platform.system() == "Darwin":  # macOS
            subprocess.call(["open", file_path])
        else:  # Linux
            subprocess.call(["xdg-open", file_path])

    def on_tree_select(self,event):
        selected_item = self.tree.focus()  # Get selected item ID
        file_path = self.tree.item(selected_item)['values'][0]  # We stored path in values
        #print(f" on_tree_select open {selected_item}")
        #print(f" on_tree_select open 1 {file_path}")
        if os.path.isfile(file_path):
            self.open_file(file_path)

    def insert_items(self,parent, path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            # Insert into the tree
            tree_id = self.tree.insert(parent, 'end', text=item, values=[item_path])
            if os.path.isdir(item_path):
                # You can recursively add subfolders if you want
                #print(f" insert_items built tree as {self.tree.item(self.tree.focus()['values'])}")
                self.insert_items(tree_id, item_path)

class SUMMJOB:
    def read_tmp_file():
        filepath=os.path.join(parse.JobPath.rootpath, 'tmp_file')

        with open(filepath, 'r') as file:
            juuid = file.readlines()

        print(f"Read SUMMJOB {filepath} cotents {juuid}")
        return juuid

    def summarize_job(jobname: str):
        print(f"SUMMJOB jobname {jobname}")
        if jobname and len(jobname) >10:
            readQuotefile.demo_qty_and_price(jobname)
        else:
            readQuotefile.demo_qty_and_price("ignore")

    def Get_JobEntry(my_entry):
        #Populate the ENtry field with value
        my_entry.delete(0,END)
        juuid = SUMMJOB.read_tmp_file()

        my_entry.insert(0, juuid)

        getresult = my_entry.get()
        print(f"Entry field value {getresult}")

        SUMMJOB.summarize_job(getresult)

def convert_job_xml_to_txt(startnode):
    for f_job in os.listdir(startnode):
        full_path = os.path.join(startnode, f_job)

        if os.path.isdir(full_path):
            convert_job_xml_to_txt(full_path)  # Recurse
            continue

        if f_job.startswith("JOB") and f_job.endswith(".xml"):
            try:
                tree = ET.parse(full_path)
                root = tree.getroot()
                pais = root.find('pais')
                if pais is None:
                    print(f"No <pais> section found in {f_job}")
                    continue

                lines = []
                for l1 in pais.findall('l1'):
                    if l1.text:
                        clean_line = l1.text.strip()
                        lines.append(clean_line)

                if lines:
                    txt_filename = f_job.replace(".xml", ".txt")
                    txt_path = os.path.join(startnode, txt_filename)
                    with open(txt_path, "w") as txtfile:
                        txtfile.write('\n'.join(lines))
                    print(f"Converted {f_job} to {txt_filename}")
                else:
                    print(f"No valid <l1> entries in {f_job}")

            except ET.ParseError as e:
                print(f"Parse error in {f_job}: {e}")
#Original JOB file has no xml tags inside and has no xml formatting.
#The file with this utility is being edited for browser readability
#Elements <JOB> is added. Indented child tag <pais> added.
#Original lines are indented with tag <l1>
def fix_Jobfile(startnode):
    xml_header: str = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<JOB>\n"
    xml_child: str ="\t<pais>\n"
    xml_element: str = "\t\t<l1>"
    xml_element_end: str = "</l1>"
    xml_end: str = "\t</pais>\n</JOB>"
    f_loc = startnode
    for f_job in os.listdir(f_loc):
        if os.path.isdir(os.path.join(startnode,f_job)):
            fix_Jobfile(os.path.join(startnode,f_job))
            pass
        else:
            f_str: str = os.path.join(startnode, f_job)

            #Detect that file name starts as JOB and ends as xml
            if (f_job[:3] == "JOB") and f_job[-3:] == "xml":
                print(f" Job file-> {os.path.join(startnode, f_job)}")
                tline=""
                #with open(os.path.join(startnode, f_job), "r") as file:
                must_update = parse.VarType.TRUE
                with open(os.path.join(startnode, f_job), "r") as file:
                    orig_content = file.read()
                    # Each line needs a new lien to be interpreted as a separate line
                    #when rendered to a browser.
                    # Hence use file.readlines() instead of file.read()

                with open(os.path.join(startnode, f_job), "r") as file:
                    original_content = file.readlines()

                print(f"TYhe first chars are already {orig_content[:5]}")
                if orig_content[:5] == "<?xml":
                    print("TYhe last chars are already xmled")
                    must_update=parse.VarType.FALSE
                    must_update = parse.VarType.FALSE
                else:
                    must_update = parse.VarType.TRUE

                tline=""
                print(f" What is must_update {must_update}")
                if must_update:
                    print("Convert file to xml")

                    for line in original_content:
                        line = xml_element + line.rstrip()  + xml_element_end +line[-1]
                        print(f" Adding tags {line}")
                        tline=tline + line
                    print(f"tline composed as {tline}")

                    with open(os.path.join(startnode, f_job), "w") as file:
                        file.write(xml_header + xml_child)

                    with open(os.path.join(startnode, f_job), "a") as file:
                        file.writelines(tline + xml_end)

            else:
                pass


def job_list():
    job_list_frame = Frame(job, height=770, width=1070)

    job_list_frame.place(x=230, y=130, width=1000, height=555)
    date_label = Label(job_list_frame,
                       text='Enter a Date'
                       )
    cal = DateEntry(job_list_frame,
                    width=20,
                    font=('arial', 20),
                    bg='darkener',
                    fg=parse.Colors.WHITE,  # 'white',
                    year=2025)
    date_label.grid()
    cal.grid()
    back_button = Button(job_list_frame,
                         text='Back',
                         font=('ubuntu', 15, 'italic'),
                         # background="bisque",
                         bg=parse.Colors.CYAN,
                         fg=parse.Colors.WHITE,
                         bd=0,
                         cursor="hand1",
                         command=lambda: job_list_frame.place_forget()
                         )
    back_button.grid(row=0, column=11)
    top_panel_frame = Frame(job_list_frame)
    top_panel_frame.place(x=0, y=70, relwidth=1, height=235)

    # Search Section Frame
    def search_section_frame():
        search_frame = Frame(top_panel_frame)
        search_frame.grid()
        search_combobox = ttk.Combobox(
            search_frame,
            values=('Job', 'TX', 'All'),
            font=('arial', 13, 'italic'),
            state='readonly',
            width=10
        )
        search_combobox.set('Search')
        search_combobox.grid(row=0, column=0, padx=10)
        search_entry = Entry(search_frame,
                             font=('arial', 13)
                             )
        search_entry.grid(row=0, column=1)

        vert_scroll = Scrollbar(top_panel_frame, orient=VERTICAL)
        hor_scroll = Scrollbar(top_panel_frame, orient=HORIZONTAL)

        day_jobs_view = ttk.Treeview(top_panel_frame,
                                     columns='File',
                                     show='headings',
                                     yscrollcommand=vert_scroll.set,
                                     xscrollcommand=hor_scroll.set
                                     )

        day_jobs_view.grid(pady=10)
        day_jobs_view.heading('File', text='Job UUID')
        day_jobs_view.column('File', width=380, minwidth=300)
        # day_jobs_view.configure(FileApp(top_panel_frame,path=path_to_my_project))

        search_button = Button(search_frame,
                               text='Search',
                               font=('arial', 13),
                               bg=parse.Colors.ICE,
                               width=10,
                               cursor='hand2'
                               , command=lambda: FileApp(day_jobs_view, path=parse.JobPath.rootpath)
                               )
        search_button.grid(row=0, column=2, padx=10)

        # Search Section Frame

    def search_summ_frame():
        juuid = SUMMJOB.read_tmp_file()
        filepath=os.path.join(parse.JobPath.rootpath, 'tmp_file')

        with open(filepath, 'r') as file:
            juuid = file.readlines()
        jobname_entry = juuid
        print(f"Read search_summ_frame {filepath} cotents {juuid}")

        print(f" Tmp file contents {juuid}")
        summ_frame = Frame(job_list_frame,
                           bg=parse.Colors.ICE)
        summ_frame.place(x=0, y=310, relwidth=1, height=30)
        summ_frame_label = Label(summ_frame,
                                     text='Job(without .xml)',
                                     font=('arial', 10),
                                     fg='black',
                                     bg=parse.Colors.ICE
                                     )
        summ_frame_label.grid(row=0, column=0)
        jobname_entry = Entry(summ_frame,
                             font=('arial', 12),
                             bg=parse.Colors.WHITE,
                             width=40
                             )
       # jobname_entry.insert(0, 'Job UUID here')
        jobname_entry.grid(row=0, column=1, padx=10 )

        summ_button = Button(summ_frame,
                                 text='<<Summarize Orders>>',
                                 font=('Arial',8,'italic'),
                                 pady=2,
                                 command=lambda: SUMMJOB.Get_JobEntry(jobname_entry)
                                 #   command=lambda: readQuotefile.demo_qty_and_price()
                                 )
        summ_button.grid(row=0, column=2)

    # Detail section
    def detail_section_frame():
        gasketimage = PhotoImage(file="images\\gaskets.png")
        detail_frame = Frame(job_list_frame,
                             # bg=parse.Colors.BLUE
                             bg=parse.Colors.RUBY
                             )
        gasketimagelabel=Label(detail_frame,
                               text="Glenn's Gaskets",
                               font=('arial', 12),
                               bg=parse.Colors.GREENMATT,
                               fg=parse.Colors.ICE)
        detail_frame.place(x=0, y=330, relwidth=1, height=255)
        gasketimagelabel.grid(row=1, column=1)
        return detail_frame

    ##Middle Questionnaire section
    def question_section_frame():
        question_frame = Frame(job_list_frame,
                               bd=4)
        question_frame.place(x=0, y=260, relwidth=1, height=115)
        question_combobox = ttk.Combobox(
            question_frame,
            values=(opt1, opt2, opt3, opt4),
            font=('arial', 13),
            state='readonly',
            width=30
        )
        question_frame_label = Label(question_frame,
                                     text='What is your choice?',
                                     font=('arial', 12),
                                     fg='black',
                                     bg=parse.Colors.ICE
                                     )
        question_frame_label.grid(row=1, column=0)
        question_combobox.set('Select One')
        question_combobox.grid(row=1, column=1)

        question_button = Button(question_frame,
                                 text='Click',
                                 command=lambda: parse.prepare_summary()
                                 )
        question_button.grid(row=1, column=2)
        #copy_button = Button(question_frame,
        #                         text='Focus on JobName and Click',
        #                         command=lambda: readQuotefile.demo_qty_and_price()
        #                         )
        #copy_button.grid(row=2, column=2)

    search_section_frame()
    detail_section_frame()
    question_section_frame()
    search_summ_frame()


# GUI
job = Tk()
obj=GaskUI(job)

#fix_Jobfile(parse.JobPath.rootpath)
job.mainloop()
