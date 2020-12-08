import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
import tkinter.messagebox
from tkinter.font import Font
from tkinter.filedialog import askopenfilename
from pandastable import Table
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GUI:

    def __init__(self, master, db):
        self.master = master
        # Create the header name
        self.head_label = tk.Label(self.master, text='Student Roster and Grade Management System')
        myfont = Font(family="Times New Roman", size=20)
        self.head_label.config(font=myfont)
        self.head_label.pack()

        ###############################
        # Create a Sample Database    #
        ###############################

        self.conn = db
        self.cur = self.conn.cursor()


        # Generate a random sample student data

        # self.cur.execute('''INSERT OR IGNORE INTO student_info(student_id ,
        #                                              class,
        #                                              name)
        #                                 Values(?,?,?)''', (95544, 'ECE502', 'Zijian Wang'))
        #
        # self.cur.execute('''INSERT OR IGNORE INTO student_info(student_id ,
        #                                              class,
        #                                              name)
        #                                 Values(?,?,?)''', (95522, 'ECE505', 'Nathan Wang'))
        #
        # self.cur.execute('''INSERT OR IGNORE INTO student_info(student_id ,
        #                                              class,
        #                                              name)
        #                                 Values(?,?,?)''', (95444, 'ECE505', 'Zsian Gang'))
        #
        # self.cur.execute('''INSERT OR IGNORE INTO student_info(student_id ,
        #                                              class,
        #                                              name)
        #                                 Values(?,?,?)''', (95022, 'ECE505', 'Nafhan Lang'))
        #
        # self.cur.execute('''INSERT OR IGNORE INTO student_info(student_id ,
        #                                              class,
        #                                              name)
        #                                 Values(?,?,?)''', (91245, 'ECE505', 'Pafhan Vang'))

        # Create a drop down menu for different classes from DB
        self.classes = self.cur.execute('SELECT DISTINCT class FROM student_info').fetchall()
        print(type(self.classes))
        print(self.classes)
        self.conn.commit()
        self.cur.close()
        # self.conn.close()

        self.classes_variable = tk.StringVar(self.master)
        self.classes_variable.set(self.classes[0])  # default value

        self.label_2 = tk.Label(self.master, text='Please select a class: ', font=('Helvetica 16 bold italic', 15))
        self.label_2.place(x=80, y=55)

        self.w = tk.OptionMenu(self.master, self.classes_variable, *self.classes)
        self.w.config(width=15, font=('Helvetica', 12))
        self.w.place(x=330, y=50)

        # Create 'Add a class' button
        self.add_a_class = tk.Button(self.master, text='Add a class', font=('Helvetica 16 bold italic', 14),
                            command=self.add_a_class, width=14)

        self.add_a_class.place(x=530, y=50)

        # Create 'Generate Class Report' button
        self.generate_report = tk.Button(self.master, text='Generate class report', font=('Helvetica 16 bold italic', 14),
                            command=self.generate_class_report, width=21)
        self.generate_report.place(x=700, y=50)

        # Generate UI
        self.main_frame = None
        self.show_ui()

        # Config main page frame
    def show_ui(self):
        if self.main_frame:
            self.main_frame.destroy()

        self.main_frame = tk.Frame(self.master, width=1050, height=750, bg="", colormap="new")
        self.main_frame.pack(side='bottom', expand=True)

        # Indicate what class is on operation

        self.label_2 = tk.Label(self.main_frame, text='You are viewing class:',
                                font=('Times New Roman', 14), bg="white")
        self.label_2.place(x=10, y=20)

        self.label_3 = tk.Label(self.main_frame, textvariable=self.classes_variable,
                                font=('Times New Roman', 14), bg="white")
        self.label_3.place(x=200, y=20)

        # Import student information button
        self.b1 = tk.Button(self.main_frame, text='Import Student Information', font=('Helvetica 16 bold italic', 15),
                            command=self.import_student_info, width=30)
        self.b1.place(x=10, y=50)

        # Add student information button
        self.b2 = tk.Button(self.main_frame, text='Add Student Information', font=('Helvetica 16 bold italic', 15),
                            command=self.add_student_info, width=30)
        self.b2.place(x=10, y=100)

        # Take Attendance
        self.b3 = tk.Button(self.main_frame, text='Take Attendance', font=('Helvetica 16 bold italic', 15),
                            command=self.take_attendance, width=30)
        self.b3.place(x=10, y=150)

        # Grade Assignments
        self.b4 = tk.Button(self.main_frame, text='Grade Assignments', font=('Helvetica 16 bold italic', 15),
                            command=self.grade_assignment, width=30)
        self.b4.place(x=10, y=200)

        # Show class grades
        self.b6 = tk.Button(self.main_frame, text='Show Class Grades', font=('Helvetica 16 bold italic', 15),
                            command=self.show_classgrade, width=30)
        self.b6.place(x=10, y=250)

        # Curve the grade and show
        self.b7 = tk.Button(self.main_frame, text='*Curve Class Grades', font=('Helvetica 16 bold italic', 15),
                            command=self.curve_classgrade, width=30)
        self.b7.place(x=10, y=300)

    def add_a_class(self):
        if self.main_frame:
            self.main_frame.destroy()

        self.main_frame = tk.Frame(self.master)
        self.main_frame['width'] = 800
        self.main_frame['height'] = 600
        self.lf = tk.LabelFrame(self.main_frame, text='Add a class', font=('Helvetica 16 bold italic', 15), width=30)
        self.className = tk.Label(self.lf, text='Class Name', font=('Helvetica 16 bold italic', 15), width=30)
        self.className.pack()
        self.class_entry = tk.Entry(self.lf, width=30)
        self.class_entry.pack()

        def cmd1():

            self.classes.append(self.class_entry.get())
            print(self.classes)
            '''
            Update the dropdown menu --- complicated
            '''
            menu = self.w["menu"]
            menu.delete(0, "end")
            for string in self.classes:
                menu.add_command(label=string, command=lambda value=string: self.classes_variable.set(value))
            self.classes_variable.set(self.class_entry.get())
            self.class_entry.delete(0, 'end')

        self.btn1 = tk.Button(self.lf, text='Return', font=('Helvetica 16 bold italic', 15), width=20, command=self.show_ui)
        self.btn1.pack(side='left')
        self.btn2 = tk.Button(self.lf, text='Submit', font=('Helvetica 16 bold italic', 15), width=20, command=cmd1)
        self.btn2.pack(side='right')
        self.lf.place(x=350, y=100)
        self.main_frame.place(x=0, y=150)

    def generate_class_report(self):

        self.final_grade_df.to_excel('Student Grade Report.xlsx', sheet_name='Grades', index=False)
        tkinter.messagebox.showinfo('Completed', 'Student Grade Report is generated!')

    def import_student_info(self):

        if self.main_frame:
            self.main_frame.destroy()

        self.main_frame = tk.Frame(self.master)
        self.main_frame['width'] = 900
        self.main_frame['height'] = 700
        self.lf = tk.LabelFrame(self.main_frame, text='Preview the data',
                                font=('Helvetica 16 bold italic', 15), width=200)

        def cmd1():
            self.cur = self.conn.cursor()

            for i in self.df.index:
                print(i)
                ID = int(self.df.loc[i, 'Student_ID'])
                class_name = str(self.df.loc[i, 'Class'])
                student_name = str(self.df.loc[i, 'Name'])

                self.cur.execute('''INSERT OR IGNORE INTO student_info(student_id ,
                                                                 class,
                                                                 name) Values(?,?,?)''', (ID, class_name, student_name))
                self.conn.commit()

            results = self.cur.execute('SELECT * FROM student_info').fetchall()
            print(results)
            self.cur.close()
            tkinter.messagebox.showinfo('Completed', 'Student roster is loaded')
            # except:
                #print("Oops!  Something went wrong")

        self.btn1 = tk.Button(self.main_frame, text='Return', font=('Helvetica 16 bold italic', 15), width=15, command=self.show_ui)
        self.btn1.place(x=350, y=520)
        self.btn2 = tk.Button(self.main_frame, text='Import', font=('Helvetica 16 bold italic', 15), width=15, command=cmd1)
        self.btn2.place(x=650, y=520)
        self.main_frame.place(x=0, y=150)
        self.lf.place(x=450, y=0)

        # Load from a csv or excel workbook
        name = askopenfilename(filetypes=[('CSV', '*.csv',), ('Excel', ('*.xls', '*.xlsx'))])

        if name:
            if name.endswith('.csv'):
                self.df = pd.read_csv(name)
            else:
                self.df = pd.read_excel(name)

        self.table = pt = Table(self.lf, dataframe=self.df, width=70, height=80,
                                showstatusbar=True, showtoolbar=True)
        pt.show()


    def add_student_info(self):

        if self.main_frame:
            self.main_frame.destroy()

        self.main_frame = tk.Frame(self.master)
        self.main_frame['width'] = 900
        self.main_frame['height'] = 700
        # Create Text boxes
        student_id = tk.Entry(self.main_frame, width=30)
        student_id.grid(row=0, column=1, padx=20)
        student_idLab = tk.Label(self.main_frame, text='Student ID', font=('Helvetica 16 bold italic', 15))
        student_idLab.grid(row=0, column=0)
        name = tk.Entry(self.main_frame, width=30)
        name.grid(row=0, column=3, padx=20)
        nameLab = tk.Label(self.main_frame, text='Student Name', font=('Helvetica 16 bold italic', 15))
        nameLab.grid(row=0, column=2)
        class_name = tk.Entry(self.main_frame, width=30, textvariable=self.classes_variable)
        class_name.grid(row=0, column=5)
        class_nameLabel = tk.Label(self.main_frame, text='Class Name', font=('Helvetica 16 bold italic', 15))
        class_nameLabel.grid(row=0, column=4)
        self.main_frame.place(x=70, y=150)

        def cmd1():

            self.cur = self.conn.cursor()
            idd = int(student_id.get())
            student_name = name.get()
            name_of_class = class_name.get()

            self.cur.execute('''INSERT OR IGNORE INTO student_info(student_id ,
                                                             class,
                                                             name) Values(?,?,?)''', (idd, name_of_class, student_name))

            self.conn.commit()
            results = self.cur.execute('''SELECT * FROM student_info WHERE student_id = (?)''', (idd,)).fetchall()
            print(results)
            self.cur.close()
            tkinter.messagebox.showinfo('Completed', 'Student info is inserted')

            student_id.delete(0, 'end')
            name.delete(0, 'end')
            class_name.delete(0, 'end')

        self.btn1 = tk.Button(self.main_frame, text='Return', font=('Helvetica 16 bold italic', 12), width=18,
                              command=self.show_ui)
        self.btn1.grid(row=1, column=1, padx=15, pady=25)
        self.btn2 = tk.Button(self.main_frame, text='Insert', font=('Helvetica 16 bold italic', 12), width=18,
                              command=cmd1)
        self.btn2.grid(row=1, column=3, padx=15, pady=25)

    def take_attendance(self):
        if self.main_frame:
            self.main_frame.destroy()

        self.main_frame = tk.Frame(self.master)
        self.main_frame['width'] = 1000
        self.main_frame['height'] = 800

        # Create the a listbox for multiple selections

        self.slb = tk.Scrollbar(self.main_frame)
        self.slb.pack(side='right', fill='y')
        self.lb = tk.Listbox(self.main_frame, yscrollcommand=self.slb.set, width=50, height=40, selectmode='multiple')

        # Get all student ID and Name and filter to the selected class
        results_df = pd.read_sql_query("SELECT * FROM student_info", self.conn)
        results_df = results_df[results_df['class'] == self.classes_variable.get()[2:8]]
        print(results_df)

        # Add to the list boxes
        for i in results_df.index:
            self.lb.insert('end', str(results_df.loc[i, 'student_id']) +
                                                                   ' ' + str(results_df.loc[i, 'name']))

        self.v = tk.IntVar()
        self.v.set(1)
        tk.Radiobutton(self.main_frame, text='Attendance Day 1', variable=self.v,
                    value=1, font=('Helvetica 16 bold italic', 12)).place(x=305, y=70)
        tk.Radiobutton(self.main_frame, text='Attendance Day 2', variable=self.v,
                    value=2, font=('Helvetica 16 bold italic', 12)).place(x=305, y=100)
        tk.Radiobutton(self.main_frame, text='Attendance Day 3', variable=self.v,
                    value=3, font=('Helvetica 16 bold italic', 12)).place(x=305, y=130)
        tk.Radiobutton(self.main_frame, text='Attendance Day 4', variable=self.v,
                    value=4, font=('Helvetica 16 bold italic', 12)).place(x=305, y=160)
        tk.Radiobutton(self.main_frame, text='Attendance Day 5', variable=self.v,
                    value=5, font=('Helvetica 16 bold italic', 12)).place(x=305, y=190)
        tk.Radiobutton(self.main_frame, text='Attendance Day 6', variable=self.v,
                    value=6, font=('Helvetica 16 bold italic', 12)).place(x=305, y=220)

        def cmd1():
            reslist = list()
            selection = self.lb.curselection()

            self.cur = self.conn.cursor()

            for i in selection:
                entrada = self.lb.get(i)[:5]
                reslist.append(entrada)

            if self.v.get() == 1:
                for idd in reslist:
                    print(self.v.get())
                    idd = int(idd)
                    print(idd)
                    self.cur.execute('''UPDATE student_info SET attendance_day_1 = 1 WHERE student_id =(?)''',
                                     (idd,))

                    self.conn.commit()
                tkinter.messagebox.showinfo('Completed', 'Student Attendance is updated')

            elif self.v.get() == 2:
                for idd in reslist:
                    print(self.v.get())
                    idd = int(idd)
                    print(idd)
                    self.cur.execute('''UPDATE student_info SET attendance_day_2 = 1 WHERE student_id =(?)''',
                                     (idd,))

                    self.conn.commit()
                tkinter.messagebox.showinfo('Completed', 'Student Attendance is updated')

            elif self.v.get() == 3:
                for idd in reslist:
                    print(self.v.get())
                    idd = int(idd)
                    print(idd)
                    self.cur.execute('''UPDATE student_info SET attendance_day_3 = 1 WHERE student_id =(?)''',
                                     (idd,))

                    self.conn.commit()
                tkinter.messagebox.showinfo('Completed', 'Student Attendance is updated')

            elif self.v.get() == 4:
                for idd in reslist:
                    print(self.v.get())
                    idd = int(idd)
                    print(idd)
                    self.cur.execute('''UPDATE student_info SET attendance_day_4 = 1 WHERE student_id =(?)''',
                                     (idd,))

                    self.conn.commit()
                tkinter.messagebox.showinfo('Completed', 'Student Attendance is updated')

            elif self.v.get() == 5:
                for idd in reslist:
                    print(self.v.get())
                    idd = int(idd)
                    print(idd)
                    self.cur.execute('''UPDATE student_info SET attendance_day_5 = 1 WHERE student_id =(?)''',
                                     (idd,))

                    self.conn.commit()
                tkinter.messagebox.showinfo('Completed', 'Student Attendance is updated')

            elif self.v.get() == 6:
                for idd in reslist:
                    print(self.v.get())
                    idd = int(idd)
                    print(idd)
                    self.cur.execute('''UPDATE student_info SET attendance_day_6 = 1 WHERE student_id =(?)''',
                                     (idd,))

                    self.conn.commit()
                tkinter.messagebox.showinfo('Completed', 'Student Attendance is updated')

            self.cur.close()

        def cmd2():
            reslist = list()
            selection = self.lb.curselection()

            self.cur = self.conn.cursor()

            for i in selection:
                entrada = self.lb.get(i)[:5]
                reslist.append(entrada)

            if self.v.get() == 1:
                for idd in reslist:
                    print(self.v.get())
                    idd = int(idd)
                    print(idd)
                    self.cur.execute('''UPDATE student_info SET attendance_day_1 = 0 WHERE student_id =(?)''',
                                     (idd,))

                    self.conn.commit()
                tkinter.messagebox.showinfo('Completed', 'Student Attendance is updated')

            elif self.v.get() == 2:
                for idd in reslist:
                    print(self.v.get())
                    idd = int(idd)
                    print(idd)
                    self.cur.execute('''UPDATE student_info SET attendance_day_2 = 0 WHERE student_id =(?)''',
                                     (idd,))

                    self.conn.commit()
                tkinter.messagebox.showinfo('Completed', 'Student Attendance is updated')

            elif self.v.get() == 3:
                for idd in reslist:
                    print(self.v.get())
                    idd = int(idd)
                    print(idd)
                    self.cur.execute('''UPDATE student_info SET attendance_day_3 = 0 WHERE student_id =(?)''',
                                     (idd,))

                    self.conn.commit()
                tkinter.messagebox.showinfo('Completed', 'Student Attendance is updated')

            elif self.v.get() == 4:
                for idd in reslist:
                    print(self.v.get())
                    idd = int(idd)
                    print(idd)
                    self.cur.execute('''UPDATE student_info SET attendance_day_4 = 0 WHERE student_id =(?)''',
                                     (idd,))

                    self.conn.commit()
                tkinter.messagebox.showinfo('Completed', 'Student Attendance is updated')

            elif self.v.get() == 5:
                for idd in reslist:
                    print(self.v.get())
                    idd = int(idd)
                    print(idd)
                    self.cur.execute('''UPDATE student_info SET attendance_day_5 = 0 WHERE student_id =(?)''',
                                     (idd,))

                    self.conn.commit()
                tkinter.messagebox.showinfo('Completed', 'Student Attendance is updated')

            elif self.v.get() == 6:
                for idd in reslist:
                    print(self.v.get())
                    idd = int(idd)
                    print(idd)
                    self.cur.execute('''UPDATE student_info SET attendance_day_6 = 0 WHERE student_id =(?)''',
                                     (idd,))

                    self.conn.commit()
                tkinter.messagebox.showinfo('Completed', 'Student Attendance is updated')

            self.cur.close()

        self.lb.pack(side='left', fill='both', expand=True)
        self.slb.config(command=self.lb.yview)
        self.main_frame.place(x=350, y=150)
        self.btn1 = tk.Button(self.main_frame, text='Return', font=('Helvetica 16 bold italic', 15), width=15, command=self.show_ui, pady=25)
        self.btn1.pack(side='bottom')
        self.btn2 = tk.Button(self.main_frame, text='Mark Attended', font=('Helvetica 16 bold italic', 15), width=15, command=cmd1, pady=25)
        self.btn2.pack(side='bottom')
        self.btn3 = tk.Button(self.main_frame, text='Mark Absent', font=('Helvetica 16 bold italic', 15), width=15, command=cmd2, pady=25)
        self.btn3.pack(side='bottom')

    def grade_assignment(self):

        if self.main_frame:
            self.main_frame.destroy()

        self.main_frame = tk.Frame(self.master)
        self.main_frame['width'] = 900
        self.main_frame['height'] = 700

        # Create Text boxes
        student_id = tk.Entry(self.main_frame, width=30)
        student_id.insert('end', 95544)
        student_id.place(x=130, y=65)
        student_idLab = tk.Label(self.main_frame, text='Student ID', font=('Helvetica 16 bold italic', 15))
        student_idLab.place(x=10, y=60)
        name = tk.Entry(self.main_frame, width=30)
        name.insert('end', 'Zijian Wang')
        name.place(x=480, y=65)
        nameLab = tk.Label(self.main_frame, text='Student Name', font=('Helvetica 16 bold italic', 15))
        nameLab.place(x=350, y=60)
        class_name = tk.Entry(self.main_frame, width=30, textvariable=self.classes_variable)
        class_name.place(x=820, y=65)
        class_nameLabel = tk.Label(self.main_frame, text='Class Name', font=('Helvetica 16 bold italic', 15))
        class_nameLabel.place(x=700, y=60)

        def check_student():

            idd = int(student_id.get())
            results_df = pd.read_sql_query("SELECT * FROM student_info", self.conn)
            results_df = results_df[results_df['student_id'] == idd]
            results_df.drop(['class'], axis=1, inplace=True)
            df = results_df.melt(id_vars=['student_id', 'name'], var_name='Assignments', value_name='Grades')
            df.sort_index(ascending=False, inplace=True)

            tree = tk.ttk.Treeview(self.main_frame)
            tree.place(x=30, y=155)
            cols = list(df.columns)
            tree["columns"] = cols
            for i in cols:
                tree.column(i, anchor="w")
                tree.heading(i, text=i, anchor='w')

            for index, row in df.iterrows():
                tree.insert("", 0, text=index, values=list(row))

        def update_grade():
            idd = int(student_id.get())
            self.cur = self.conn.cursor()
            sa1 = int(e1.get())
            sa2 = int(e2.get())
            sa3 = int(e3.get())
            sa4 = int(e4.get())
            project = int(e5.get())
            exam = int(e6.get())

            self.cur.execute('''UPDATE student_info SET signature_assignment_1 = ?,
                                                        signature_assignment_2 = ?,
                                                        signature_assignment_3 = ?,
                                                        signature_assignment_4 = ?,
                                                        final_project = ?,
                                                        final_exam = ?
                                                        WHERE student_id = ?''',
                             (sa1, sa2, sa3, sa4, project, exam, idd))

            self.conn.commit()
            self.cur.close()
            tkinter.messagebox.showinfo('Completed', 'Student Grades have been updated')

        self.btn1 = tk.Button(self.main_frame, text='Return', font=('Helvetica 16 bold italic', 12), width=12,
                              command=self.show_ui, pady=12, padx = 15)
        self.btn1.place(x=200, y=100)
        self.btn2 = tk.Button(self.main_frame, text='Check Student', font=('Helvetica 16 bold italic', 12), width=12,
                              command=check_student, pady=12, padx = 15)
        self.btn2.place(x=650, y=100)

        # Create Text boxes for update grades

        tk.Label(self.main_frame, text='Assignment 1', font=('Helvetica 16 bold italic', 15)).place(x=50, y=400)
        tk.Label(self.main_frame, text='Assignment 2', font=('Helvetica 16 bold italic', 15)).place(x=500, y=400)
        tk.Label(self.main_frame, text='Assignment 3', font=('Helvetica 16 bold italic', 15)).place(x=50, y=500)
        tk.Label(self.main_frame, text='Assignment 4', font=('Helvetica 16 bold italic', 15)).place(x=500, y=500)
        tk.Label(self.main_frame, text='Final Project', font=('Helvetica 16 bold italic', 15)).place(x=50, y=600)
        tk.Label(self.main_frame, text='Final Exam', font=('Helvetica 16 bold italic', 15)).place(x=500, y=600)

        e1 = tk.Entry(self.main_frame, width=30)
        e1.place(x=250, y=405)
        e1.insert('end', 10)
        e2 = tk.Entry(self.main_frame, width=30)
        e2.place(x=700, y=405)
        e2.insert('end', 10)
        e3 = tk.Entry(self.main_frame, width=30)
        e3.place(x=250, y=505)
        e3.insert('end', 10)
        e4 = tk.Entry(self.main_frame, width=30)
        e4.place(x=700, y=505)
        e4.insert('end', 10)
        e5 = tk.Entry(self.main_frame, width=30)
        e5.place(x=250, y=605)
        e5.insert('end', 15)
        e6 = tk.Entry(self.main_frame, width=30)
        e6.place(x=700, y=605)
        e6.insert('end', 30)

        self.btn3 = tk.Button(self.main_frame, text='Update Grades', font=('Helvetica 16 bold italic', 12), width=12,
                              command=update_grade, pady=12, padx=15)
        self.btn3.place(x=430, y=650)

        self.main_frame.place(x=70, y=100)


    def show_classgrade(self):

        self.second_frame = tk.Frame(self.main_frame, width=500, height=500, bg="", colormap="new")
        self.second_frame.place(x=160, y=340)

        # qry = 'SELECT *, ' \
        #       '((signature_assignment_1+signature_assignment_2+signature_assignment_3+signature_assignment_4)/40)*45 AS SA_grade,' \
        #       '((attendance_day_1+attendance_day_2+attendance_day_3+attendance_day_4+attendance_day_5+attendance_day_6)/6)*10 AS att_grade from student_info'

        qry = 'SELECT * from student_info'
        df = pd.read_sql_query(qry, self.conn)
        df = df[df['class'] == self.classes_variable.get()[2:8]]
        df['SA_grade'] = (df.signature_assignment_1 + df.signature_assignment_2 + df.signature_assignment_3 + df.signature_assignment_4)/40*45
        df['att_grade'] = (df.attendance_day_1 + df.attendance_day_2 + df.attendance_day_3 + df.attendance_day_4)/6*10
        df['total_grade'] = df.SA_grade + df.att_grade + df.final_project + df.final_exam
        self.final_grade_df = df

        conditions = [
            (df['total_grade'] < 60),
            (df['total_grade'] >= 60) & (df['total_grade'] <= 62.99999),
            (df['total_grade'] >= 63) & (df['total_grade'] <= 67.99999),
            (df['total_grade'] >= 68) & (df['total_grade'] <= 69.99999),
            (df['total_grade'] >= 70) & (df['total_grade'] <= 72.99999),
            (df['total_grade'] >= 73) & (df['total_grade'] <= 77.99999),
            (df['total_grade'] >= 78) & (df['total_grade'] <= 79.99999),
            (df['total_grade'] >= 80) & (df['total_grade'] <= 82.99999),
            (df['total_grade'] >= 83) & (df['total_grade'] <= 87.99999),
            (df['total_grade'] >= 88) & (df['total_grade'] <= 89.99999),
            (df['total_grade'] >= 90) & (df['total_grade'] <= 92.99999),
            (df['total_grade'] >= 93) & (df['total_grade'] <= 96.99999),
            (df['total_grade'] >= 97)
        ]
        # create a list of the values we want to assign for each condition
        values = ['F', 'D-', 'D', 'D+', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'A+']
        # create a new column and use np.select to assign values to it using our lists as arguments
        df['letter_grade'] = np.select(conditions, values)
        figure1 = plt.Figure(figsize=(7, 4), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self.second_frame)
        bar1.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH)
        df.groupby('letter_grade').agg('count').reset_index().plot(kind='bar', x='letter_grade', y='student_id', ax=ax1, rot=0, legend=False)
        ax1.set_xlabel("")
        ax1.set_title('Letter Grade Distribution')

    def curve_classgrade(self):

        if self.second_frame:
            self.second_frame.destroy()

        self.second_frame = tk.Frame(self.main_frame, width=500, height=500, bg="", colormap="new")
        self.second_frame.place(x=160, y=340)

        qry = 'SELECT * from student_info'
        df = pd.read_sql_query(qry, self.conn)
        df = df[df['class'] == self.classes_variable.get()[2:8]]
        df['SA_grade'] = (df.signature_assignment_1 + df.signature_assignment_2 + df.signature_assignment_3 + df.signature_assignment_4)/40*45
        df['att_grade'] = (df.attendance_day_1 + df.attendance_day_2 + df.attendance_day_3 + df.attendance_day_4)/6*10
        df['total_grade'] = df.SA_grade + df.att_grade + df.final_project + df.final_exam
        df['curved_total_grade'] = ((df.total_grade/100)**0.5)*100
        df['total_grade'] = df['curved_total_grade']
        self.final_grade_df = df

        conditions = [
            (df['total_grade'] < 60),
            (df['total_grade'] >= 60) & (df['total_grade'] <= 62.99999),
            (df['total_grade'] >= 63) & (df['total_grade'] <= 67.99999),
            (df['total_grade'] >= 68) & (df['total_grade'] <= 69.99999),
            (df['total_grade'] >= 70) & (df['total_grade'] <= 72.99999),
            (df['total_grade'] >= 73) & (df['total_grade'] <= 77.99999),
            (df['total_grade'] >= 78) & (df['total_grade'] <= 79.99999),
            (df['total_grade'] >= 80) & (df['total_grade'] <= 82.99999),
            (df['total_grade'] >= 83) & (df['total_grade'] <= 87.99999),
            (df['total_grade'] >= 88) & (df['total_grade'] <= 89.99999),
            (df['total_grade'] >= 90) & (df['total_grade'] <= 92.99999),
            (df['total_grade'] >= 93) & (df['total_grade'] <= 96.99999),
            (df['total_grade'] >= 97)
        ]
        # create a list of the values we want to assign for each condition
        values = ['F', 'D-', 'D', 'D+', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'A+']
        # create a new column and use np.select to assign values to it using our lists as arguments
        df['letter_grade'] = np.select(conditions, values)

        figure1 = plt.Figure(figsize=(7, 4), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self.second_frame)
        bar1.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH)
        df.groupby('letter_grade').agg('count').reset_index().plot(kind='bar', x='letter_grade', y='student_id', ax=ax1,
                                                                   rot=0, legend=False)
        ax1.set_xlabel("")
        ax1.set_title('Curved Letter Grade Distribution')





