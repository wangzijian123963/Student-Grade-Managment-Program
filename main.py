import tkinter as tk
from UI import GUI
import sqlite3
import random

make_sample_data = True

if __name__ == '__main__':
    # Crate or connect to the database
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    # Create the default table for ECE502 class
    cur.execute('''CREATE TABLE IF NOT EXISTS student_info (student_id Integer Primary Key Not Null,
                                                                         class TEXT,
                                                                         name TEXT,
                                                                         attendance_day_1 INT DEFAULT 1,
                                                                         attendance_day_2 INT DEFAULT 1,
                                                                         attendance_day_3 INT DEFAULT 1,
                                                                         attendance_day_4 INT DEFAULT 1,
                                                                         attendance_day_5 INT DEFAULT 1,
                                                                         attendance_day_6 INT DEFAULT 1,
                                                                         signature_assignment_1 INT DEFAULT 0,
                                                                         signature_assignment_2 INT DEFAULT 0,
                                                                         signature_assignment_3 INT DEFAULT 0,
                                                                         signature_assignment_4 INT DEFAULT 0,
                                                                         final_project INT DEFAULT 0,
                                                                         final_exam FLOAT DEFAULT 0)''')

    conn.commit()

    if make_sample_data == True:
        # Generate 200 random numbers between 10000 and 99999 as student ID number
        idlist = random.sample(range(10000, 99999), 200)
        # Generate 200 random numbers between 0 and 1 as attendance
        att_1 = [random.randint(0, 1) for i in range(200)]
        att_2 = [random.randint(0, 1) for i in range(200)]
        att_3 = [random.randint(0, 1) for i in range(200)]
        att_4 = [random.randint(0, 1) for i in range(200)]
        att_5 = [random.randint(0, 1) for i in range(200)]
        att_6 = [random.randint(0, 1) for i in range(200)]
        # Generate 200 random numbers between 5 and 10 as signature assignments
        sa_1 = [random.randint(5, 10) for i in range(200)]
        sa_2 = [random.randint(5, 10) for i in range(200)]
        sa_3 = [random.randint(5, 10) for i in range(200)]
        sa_4 = [random.randint(5, 10) for i in range(200)]
        # Generate 200 random numbers between 10 and 15 as final_project
        fp = [random.randint(10, 15) for i in range(200)]
        # Generate 200 random numbers between 20 and 30 as final_exam
        fe = [random.randint(20, 30) for i in range(200)]
        # Generate 200 classes
        classes = ['ECE502' for i in range(100)] + ['ECE505' for i in range(100)]
        # Generate 200 names
        names = ['John Smith' for i in range(200)]

        cur.execute('''INSERT OR IGNORE INTO student_info(student_id ,
                                                     class,
                                                     name)
                                        Values(?,?,?)''', (95544, 'ECE502', 'Zijian Wang'))
        conn.commit()

        for i in range(200):
            print(i)
            cur.execute('''INSERT OR IGNORE INTO student_info(   student_id ,
                                                                 class,
                                                                 name,
                                                                 attendance_day_1,
                                                                 attendance_day_2,
                                                                 attendance_day_3,
                                                                 attendance_day_4,
                                                                 attendance_day_5,
                                                                 attendance_day_6,
                                                                 signature_assignment_1,
                                                                 signature_assignment_2,
                                                                 signature_assignment_3,
                                                                 signature_assignment_4,
                                                                 final_project,
                                                                 final_exam)
                                                    Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                        (idlist[i], classes[i], names[i], att_1[i], att_2[i], att_3[i], att_4[i], att_5[i], att_6[i],
                         sa_1[i], sa_2[i], sa_3[i], sa_4[i], fp[i], fe[i]))
            conn.commit()

        cur.close()

    m = tk.Tk()
    m.geometry('1300x1100')
    m.title("Student Roster and Grade Management System")
    GUI(master=m, db=conn)
    m.mainloop()
