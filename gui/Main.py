###################
# Imports
###################
# External files
from Tkinter import *
import tkMessageBox
from PIL import Image,ImageTk
import rpy2.robjects as robjects
import random

# Homemade files
import Point
import Pointer_List
import Clusters_value

###################
# Globals
###################
cluster_choice = 0 # 0 is for k_modes
cluster_values = Clusters_value.Cluster_value(cluster_choice)

###################
# Functions
###################
def do_nothing():
    pass

def toggle(var):
    if var.get() == 0:
        var.set(1)
    elif var.get() == 1:
        var.set(0)

def run_r(value):
    r = robjects.r
    r.source("test.R")
    fn = r['predict']
    result = fn(value.info_vector)

    return result

def output_dialog(output):
    msg = "Thank you very much for using our application! It was hard work for all of us and I hope it gave you the" \
          " result you hoped for!"

    tkMessageBox.showinfo(message=msg)

    output.destroy()

def reset_checks(checks):
    for key, value in checks.iteritems():
        for question in value:
            for answer in question:
                del answer

def check_entry(entries):
    for key, value in entries.iteritems():
        if not value.get():
            return False
    return True

def check_checks(checks):
    for question in checks:
        count = 0
        for answer in question:
            if answer.get() == 1:
                count += 1
        if count == 0 or count > 1:
            return False

    return True

def clear_entry(entries, checks):
    for key, value in entries.iteritems():
        value.delete(0,END)

    for key, value in checks.iteritems():
        value.deselect()

def submit_entry(entry, entries, checks):
    if not check_entry(entries):
        tkMessageBox.showerror(message="Please enter all data: All fields must have valid data.")
    elif not check_checks(checks['fc']):
        tkMessageBox.showerror(message="Error in Financial Concerns: All questions must have one and only one checkbox marked.")
    elif not check_checks(checks['ae']):
        tkMessageBox.showerror(message="Error in Academic Engagement: All questions must have one and only one checkbox marked.")
    elif not check_checks(checks['ic']):
        tkMessageBox.showerror(message="Error in Institutional Commitment: All questions must have one and only one checkbox marked.")
    elif not check_checks(checks['grit']):
        tkMessageBox.showerror(message="Error in GRIT: All questions must have one and only one checkbox marked.")
    else:
        # reset all check boxes
        reset_checks(checks)

        # Create the new point
        new_point = Point.Point(entries, checks)

        # Find the cluster value that corresponds to this point
        new_point.cluster_name = cluster_values.find_closest(new_point)

        # classify the cluster
        #result = run_r(new_point.info_vector)

        # Destroy window
        entry.destroy()

        # send this data point to output view - TODO STUB CODE GET RID OF
        stub = True
        if new_point.major == 'FAIL':
            stub = False

        run_output_view(stub)

def create_tutorial_pages(tut):
    pages = Pointer_List.pointer_list()

    p1 = Frame(tut)
    p2 = Frame(tut)
    p3 = Frame(tut)
    p4 = Frame(tut)
    p5 = Frame(tut)
    p6 = Frame(tut)
    p7 = Frame(tut)
    p8 = Frame(tut)
    p9 = Frame(tut)
    p10 = Frame(tut)


    p1.grid(row=1, column=0, sticky='news')
    p2.grid(row=1, column=0, sticky='news')
    p3.grid(row=1, column=0, sticky='news')
    p4.grid(row=1, column=0, sticky='news')
    p5.grid(row=1, column=0, sticky='news')
    p6.grid(row=1, column=0, sticky='news')
    p7.grid(row=1, column=0, sticky='news')
    p8.grid(row=1, column=0, sticky='news')
    p9.grid(row=1, column=0, sticky='news')
    p10.grid(row=1, column=0, sticky='news')

    #####
    ##### Page 1
    msg = ('Welcome to the tutorial! \n \n'
            'This application will attempt to classify whether or not a new student will likely stay in school at OU.\n'
            'This will be accomplished through a series of Data Mining techniques called clustering and classification.\n \n'
            'Thousands of other students data were collected in order to try and find a trend on whether or not they would be retained. \n '
            'Using this data, we can take new student entries and say with a certain confidence whether or not \n'
            'the student will be likely to continue in their studies. \n'
            'If not is the answer, perhaps they could be encouraged to seek other courses, another major, or perhaps \n'
            'more aid in order to succeed.')

    Message(p1, text=msg).pack()

    #####
    ##### Page 2
    msg = "To discover whether or not a student will be retained, start by clicking 'Add New Student' on the main page \n"
    Label(p2, text=msg).grid(row=0,column=1)

    bck_ground_image = ImageTk.PhotoImage(file='main_tut.png')
    bck_ground_label = Label(p2, image=bck_ground_image)
    bck_ground_label.grid(row=2,column=1)
    bck_ground_label.image = bck_ground_image

    #####
    ##### Page 3
    msg = ('Now, fill out each entry with the appropriate data. If no data is available, input ".". No field can be empty. \n'
            'Click "Next"')
    Message(p3, text=msg).grid(row=0,column=1)

    bck_ground_image = ImageTk.PhotoImage(file='tut_1.png')
    bck_ground_label = Label(p3, image=bck_ground_image)
    bck_ground_label.grid(row=2,column=1)
    bck_ground_label.image = bck_ground_image

    #####
    ##### Page 4
    msg = ('Notice: If you fill out an entry with an invalid type an error message will occur. \n'
           'Simply click "ok" and continue filling out the form.')
    Message(p4, text=msg).grid(row=0,column=1)

    bck_ground_image = ImageTk.PhotoImage(file='tut_2.png')
    bck_ground_label = Label(p4, image=bck_ground_image)
    bck_ground_label.grid(row=2,column=1)
    bck_ground_label.image = bck_ground_image

    #####
    ##### Page 5
    msg = ('Next you will continue through four surveys that you must complete. After choosing your answer, click "Next"')
    Message(p5, text=msg).grid(row=0,column=1)

    bck_ground_image = ImageTk.PhotoImage(file='tut_3.png')
    bck_ground_label = Label(p5, image=bck_ground_image)
    bck_ground_label.grid(row=2,column=1)
    bck_ground_label.image = bck_ground_image

    #####
    ##### Page 6
    msg = ('Notice: If you fill out a survey with more than one check per question, an error will occur. \n'
           'Simply click "ok" and continue filling out the form correctly.')
    Message(p6, text=msg).grid(row=0,column=1)

    bck_ground_image = ImageTk.PhotoImage(file='tut_4.png')
    bck_ground_label = Label(p6, image=bck_ground_image)
    bck_ground_label.grid(row=2,column=1)
    bck_ground_label.image = bck_ground_image

    #####
    ##### Page 7
    msg = ('Notice: If you fill out a survey question with no entries, an error will occur. \n'
           'Simply click "ok" and continue filling out the form correctly.')
    Message(p7, text=msg).grid(row=0,column=1)

    bck_ground_image = ImageTk.PhotoImage(file='tut_5.png')
    bck_ground_label = Label(p7, image=bck_ground_image)
    bck_ground_label.grid(row=2,column=1)
    bck_ground_label.image = bck_ground_image

    #####
    ##### Page 8
    msg = ('Once you reach and complete all pages (1 field page and 4 surveys) you can submit. \n'
           'Simply click "Submit"')
    Message(p8, text=msg).pack(side=TOP)

    #####
    ##### Page 9
    msg = ('Next your classification will be prompted! Here is a student that is expected to be retained. \n'
           'Simply click "done" to finish')
    Message(p9, text=msg).grid(row=0,column=1)

    bck_ground_image = ImageTk.PhotoImage(file='tut_6.png')
    bck_ground_label = Label(p9, image=bck_ground_image)
    bck_ground_label.grid(row=2,column=1)
    bck_ground_label.image = bck_ground_image

    #####
    ##### Page 10
    msg = ('Unfortunately, not every student will be predicted to be retained. Here is an example: \n'
           'Simply click "done" to finish.')
    Message(p10, text=msg).grid(row=0,column=1)

    bck_ground_image = ImageTk.PhotoImage(file='tut_7.png')
    bck_ground_label = Label(p10, image=bck_ground_image)
    bck_ground_label.grid(row=2,column=1)
    bck_ground_label.image = bck_ground_image


    # Add the pages to the pointer list
    pages.add(p1)
    pages.add(p2)
    pages.add(p3)
    pages.add(p4)
    pages.add(p5)
    pages.add(p6)
    pages.add(p7)
    pages.add(p8)
    pages.add(p9)
    pages.add(p10)

    return pages

def create_entry_page(e):
    entry = Frame(e)

    entry.grid(row=1, column=0, sticky='news')

    # List of all the entry fields
    entries = {}

    Label(entry, text="Please enter all data.").grid(row=0,column=0)

    # Add all of the labels needed
    act_sat_conv_lbl =          Label(entry, text="ACT-SAT Conversion").grid(row=1, column=0)
    ap_hours_lbl =              Label(entry, text="AP Hours").grid(row=2, column=0)
    hs_gpa_lbl =                Label(entry, text="HS GPA").grid(row=3, column=0)
    trig_lbl =                  Label(entry, text="Trig").grid(row=4, column=0)
    alg_1_lbl =                 Label(entry, text="Alg I").grid(row=5, column=0)
    alg_2_lbl =                 Label(entry, text="Alg II").grid(row=6, column=0)
    alg_coll_lbl =              Label(entry, text="Coll Alg").grid(row=7, column=0)
    geometry_lbl =              Label(entry, text="Geometry").grid(row=8, column=0)
    pre_calc_lbl =              Label(entry, text="Pre-Calc").grid(row=9, column=0)
    stats_lbl =                 Label(entry, text="Stats").grid(row=10, column=0)
    math_senior_lbl =           Label(entry, text="Math Senior").grid(row=11, column=0)
    t_course_1_lbl =            Label(entry, text="Title: Course 1").grid(row=1, column=2)
    t_course_2_lbl =            Label(entry, text="Title: Course 2").grid(row=2, column=2)
    t_course_3_lbl =            Label(entry, text="Title: Course 3").grid(row=3, column=2)
    t_course_4_lbl =            Label(entry, text="Title: Course 4").grid(row=4, column=2)
    t_course_5_lbl =            Label(entry, text="Title: Course 5").grid(row=5, column=2)
    t_course_6_lbl =            Label(entry, text="Title: Course 6").grid(row=6, column=2)
    t_course_7_lbl =            Label(entry, text="Title: Course 7").grid(row=7, column=2)
    major_lbl =                 Label(entry, text="Major").grid(row=1, column=4)

    # Add entry fields
    act_sat_conv_entry =        Entry(entry, bd=5)
    ap_hours_entry =            Entry(entry, bd=5)
    hs_gpa_entry =              Entry(entry, bd=5)
    trig_entry =                Entry(entry, bd=5)
    alg_1_entry =               Entry(entry, bd=5)
    alg_2_entry =               Entry(entry, bd=5)
    alg_coll_entry =            Entry(entry, bd=5)
    geometry_entry =            Entry(entry, bd=5)
    pre_calc_entry =            Entry(entry, bd=5)
    stats_entry =               Entry(entry, bd=5)
    math_senior_entry =         Entry(entry, bd=5)
    t_course_1_entry =          Entry(entry, bd=5)
    t_course_2_entry =          Entry(entry, bd=5)
    t_course_3_entry =          Entry(entry, bd=5)
    t_course_4_entry =          Entry(entry, bd=5)
    t_course_5_entry =          Entry(entry, bd=5)
    t_course_6_entry =          Entry(entry, bd=5)
    t_course_7_entry =          Entry(entry, bd=5)
    major_entry =               Entry(entry, bd=5)

    # Place entry & checkbox fields in appropriate locations
    act_sat_conv_entry.grid(row=1, column=1)
    ap_hours_entry.grid(row=2, column=1)
    hs_gpa_entry.grid(row=3, column=1)
    trig_entry.grid(row=4, column=1)
    alg_1_entry.grid(row=5, column=1)
    alg_2_entry.grid(row=6, column=1)
    alg_coll_entry.grid(row=7, column=1)
    geometry_entry.grid(row=8, column=1)
    pre_calc_entry.grid(row=9, column=1)
    stats_entry.grid(row=10, column=1)
    math_senior_entry.grid(row=11, column=1)
    t_course_1_entry.grid(row=1, column=3)
    t_course_2_entry.grid(row=2, column=3)
    t_course_3_entry.grid(row=3, column=3)
    t_course_4_entry.grid(row=4, column=3)
    t_course_5_entry.grid(row=5, column=3)
    t_course_6_entry.grid(row=6, column=3)
    t_course_7_entry.grid(row=7, column=3)
    major_entry.grid(row=1, column=5)

    # Add entries to the lists
    entries['act_sat_conv_entry']       = act_sat_conv_entry
    entries['ap_hours_entry']           = ap_hours_entry
    entries['hs_gpa_entry']             = hs_gpa_entry
    entries['trig_entry']               = trig_entry
    entries['alg_1_entry']              = alg_1_entry
    entries['alg_2_entry']              = alg_2_entry
    entries['alg_coll_entry']           = alg_coll_entry
    entries['geometry_entry']           = geometry_entry
    entries['pre_calc_entry']           = pre_calc_entry
    entries['stats_entry']              = stats_entry
    entries['math_senior_entry']        = math_senior_entry
    entries['t_course_1_entry']         = t_course_1_entry
    entries['t_course_2_entry']         = t_course_2_entry
    entries['t_course_3_entry']         = t_course_3_entry
    entries['t_course_4_entry']         = t_course_4_entry
    entries['t_course_5_entry']         = t_course_5_entry
    entries['t_course_6_entry']         = t_course_6_entry
    entries['t_course_7_entry']         = t_course_7_entry
    entries['major_entry']              = major_entry

    # dummy labels - ignore these - for formatting only
    Label(entry, text="").grid(row=12,column=0)
    Label(entry, text="").grid(row=12,column=1)
    Label(entry, text="").grid(row=13,column=0)
    Label(entry, text="").grid(row=13,column=1)
    Label(entry, text="").grid(row=14,column=0)
    Label(entry, text="").grid(row=14,column=1)
    Label(entry, text="").grid(row=15,column=0)
    Label(entry, text="").grid(row=15,column=1)
    Label(entry, text="").grid(row=16,column=0)
    Label(entry, text="").grid(row=16,column=1)
    Label(entry, text="").grid(row=17,column=0)
    Label(entry, text="").grid(row=17,column=1)
    Label(entry, text="").grid(row=18,column=0)
    Label(entry, text="").grid(row=18,column=1)
    Label(entry, text="").grid(row=9,column=2)
    Label(entry, text="").grid(row=9,column=3)
    Label(entry, text="").grid(row=10,column=2)
    Label(entry, text="").grid(row=10,column=3)
    Label(entry, text="").grid(row=11,column=2)
    Label(entry, text="").grid(row=11,column=3)
    Label(entry, text="").grid(row=12,column=2)
    Label(entry, text="").grid(row=12,column=3)
    Label(entry, text="").grid(row=13,column=2)
    Label(entry, text="").grid(row=13,column=3)
    Label(entry, text="").grid(row=14,column=2)
    Label(entry, text="").grid(row=14,column=3)
    Label(entry, text="").grid(row=15,column=2)
    Label(entry, text="").grid(row=15,column=3)
    Label(entry, text="").grid(row=16,column=2)
    Label(entry, text="").grid(row=16,column=3)
    Label(entry, text="").grid(row=17,column=2)
    Label(entry, text="").grid(row=17,column=3)
    Label(entry, text="").grid(row=18,column=2)
    Label(entry, text="").grid(row=18,column=3)
    Label(entry, text="").grid(row=2,column=4)
    Label(entry, text="").grid(row=2,column=5)
    Label(entry, text="").grid(row=3,column=4)
    Label(entry, text="").grid(row=3,column=5)
    Label(entry, text="").grid(row=4,column=4)
    Label(entry, text="").grid(row=4,column=5)
    Label(entry, text="").grid(row=5,column=4)
    Label(entry, text="").grid(row=5,column=5)
    Label(entry, text="").grid(row=6,column=4)
    Label(entry, text="").grid(row=6,column=5)
    Label(entry, text="").grid(row=7,column=4)
    Label(entry, text="").grid(row=7,column=5)


    return entry, entries

def create_survey_pages(e):
    pages = []
    checks = {}

    p1 = Frame(e)
    p2 = Frame(e)
    p3 = Frame(e)
    p4 = Frame(e)

    p1.grid(row=1, column=0, sticky='news')
    p2.grid(row=1, column=0, sticky='news')
    p3.grid(row=1, column=0, sticky='news')
    p4.grid(row=1, column=0, sticky='news')

    #
    ##### FC Page

    # Top of page text
    Label(p1, text="Financial Concerns").place(relx=.5, rely=0, anchor=N)

    # information labels
    msg = ('Please rate each of the following in terms of how difficult you think the adjustment may be during your first '
           'year at OU.')
    Label(p1, text=msg).place(relx=.5, rely=.1, anchor=N)

    msg = ('Please indicate the extent to which you agree or disagree with each of the following items.')
    Label(p1, text=msg).place(relx=.5, rely=.3, anchor=N)

    msg = ('Please indicate how important each of the following was in your decision to attend OU.')
    Label(p1, text=msg).place(relx=.5, rely=.6, anchor=N)

    # labels
    q1_lbl = Label(p1, text="Having enough money:").place(relx=0, rely=.15, anchor=W)
    q2_lbl = Label(p1, text="I need to work to afford to go to school:").place(relx=0, rely=.35, anchor=W)
    q3_lbl = Label(p1, text="At the present time, I have enough financial resources to complete my first year at OU:").place(relx=0, rely=.45, anchor=W)
    q4_lbl = Label(p1, text="Financial aid received:").place(relx=0, rely=.65, anchor=W)

    # checkbox variables
    fc_q1_cb_1_val = IntVar()
    fc_q1_cb_2_val = IntVar()
    fc_q1_cb_3_val = IntVar()
    fc_q1_cb_4_val = IntVar()
    fc_q1_cb_5_val = IntVar()

    fc_q2_cb_1_val = IntVar()
    fc_q2_cb_2_val = IntVar()
    fc_q2_cb_3_val = IntVar()
    fc_q2_cb_4_val = IntVar()
    fc_q2_cb_5_val = IntVar()

    fc_q3_cb_1_val = IntVar()
    fc_q3_cb_2_val = IntVar()
    fc_q3_cb_3_val = IntVar()
    fc_q3_cb_4_val = IntVar()
    fc_q3_cb_5_val = IntVar()

    fc_q4_cb_1_val = IntVar()
    fc_q4_cb_2_val = IntVar()
    fc_q4_cb_3_val = IntVar()
    fc_q4_cb_4_val = IntVar()

    # checkboxes
    fc_q1_cb_1 = Checkbutton(p1, text="Very Easy", command=lambda: toggle(fc_q1_cb_1_val))
    fc_q1_cb_2 = Checkbutton(p1, text="Easy", command=lambda: toggle(fc_q1_cb_2_val))
    fc_q1_cb_3 = Checkbutton(p1, text="Neutral", command=lambda: toggle(fc_q1_cb_3_val))
    fc_q1_cb_4 = Checkbutton(p1, text="Difficult", command=lambda: toggle(fc_q1_cb_4_val))
    fc_q1_cb_5 = Checkbutton(p1, text="Very Difficult", command=lambda: toggle(fc_q1_cb_5_val))

    fc_q2_cb_1 = Checkbutton(p1, text="Strongly Agree", command=lambda: toggle(fc_q2_cb_1_val))
    fc_q2_cb_2 = Checkbutton(p1, text="Agree", command=lambda: toggle(fc_q2_cb_2_val))
    fc_q2_cb_3 = Checkbutton(p1, text="Neutral", command=lambda: toggle(fc_q2_cb_3_val))
    fc_q2_cb_4 = Checkbutton(p1, text="Disagree", command=lambda: toggle(fc_q2_cb_4_val))
    fc_q2_cb_5 = Checkbutton(p1, text="Strongly Disagree", command=lambda: toggle(fc_q2_cb_5_val))

    fc_q3_cb_1 = Checkbutton(p1, text="Strongly Agree", command=lambda: toggle(fc_q3_cb_1_val))
    fc_q3_cb_2 = Checkbutton(p1, text="Agree", command=lambda: toggle(fc_q3_cb_2_val))
    fc_q3_cb_3 = Checkbutton(p1, text="Neutral", command=lambda: toggle(fc_q3_cb_3_val))
    fc_q3_cb_4 = Checkbutton(p1, text="Disagree", command=lambda: toggle(fc_q3_cb_4_val))
    fc_q3_cb_5 = Checkbutton(p1, text="Strongly Disagree", command=lambda: toggle(fc_q3_cb_5_val))

    fc_q4_cb_1 = Checkbutton(p1, text="Extremely Important", command=lambda: toggle(fc_q4_cb_1_val))
    fc_q4_cb_2 = Checkbutton(p1, text="Important", command=lambda: toggle(fc_q4_cb_2_val))
    fc_q4_cb_3 = Checkbutton(p1, text="Relatively Unimportant", command=lambda: toggle(fc_q4_cb_3_val))
    fc_q4_cb_4 = Checkbutton(p1, text="Totally Unimportant", command=lambda: toggle(fc_q4_cb_4_val))

    # Place checkboxes
    fc_q1_cb_1.place(relx=.17, rely=.2, anchor=W)
    fc_q1_cb_2.place(relx=.35, rely=.2, anchor=W)
    fc_q1_cb_3.place(relx=.45, rely=.2, anchor=W)
    fc_q1_cb_4.place(relx=.6, rely=.2, anchor=W)
    fc_q1_cb_5.place(relx=.75, rely=.2, anchor=W)

    fc_q2_cb_1.place(relx=.17, rely=.4, anchor=W)
    fc_q2_cb_2.place(relx=.34, rely=.4, anchor=W)
    fc_q2_cb_3.place(relx=.44, rely=.4, anchor=W)
    fc_q2_cb_4.place(relx=.54, rely=.4, anchor=W)
    fc_q2_cb_5.place(relx=.65, rely=.4, anchor=W)

    fc_q3_cb_1.place(relx=.17, rely=.5, anchor=W)
    fc_q3_cb_2.place(relx=.34, rely=.5, anchor=W)
    fc_q3_cb_3.place(relx=.44, rely=.5, anchor=W)
    fc_q3_cb_4.place(relx=.54, rely=.5, anchor=W)
    fc_q3_cb_5.place(relx=.65, rely=.5, anchor=W)

    fc_q4_cb_1.place(relx=.17, rely=.7, anchor=W)
    fc_q4_cb_2.place(relx=.36, rely=.7, anchor=W)
    fc_q4_cb_3.place(relx=.50, rely=.7, anchor=W)
    fc_q4_cb_4.place(relx=.72, rely=.7, anchor=W)

    #
    #### Academic Engagement page

    # Top of page text
    Label(p2, text="Academic Engagement").place(relx=.5, rely=0, anchor=N)

    # information labels
    msg = ('Please indicate the extent to which you agree or disagree.')
    Label(p2, text=msg).place(relx=.5, rely=.1, anchor=N)

    msg = ('Please indicate how often you did each of the following while in high school.')
    Label(p2, text=msg).place(relx=.5, rely=.3, anchor=N)


    # labels
    q1_lbl = Label(p2, text="I rarely studied outside of class in high school:").place(relx=0, rely=.15, anchor=W)
    q2_lbl = Label(p2, text="Felt bored in class:").place(relx=0, rely=.35, anchor=W)
    q3_lbl = Label(p2, text="Went to class without doing homework or assignments:").place(relx=0, rely=.45, anchor=W)
    q4_lbl = Label(p2, text="Waited until the last minute to do my assignments:").place(relx=0, rely=.55, anchor=W)
    q5_lbl = Label(p2, text="Went late to class:").place(relx=0, rely=.65, anchor=W)
    q6_lbl = Label(p2, text="Went to class without doing assinged reading:").place(relx=0, rely=.75, anchor=W)

    # checkbox variables
    ae_q1_cb_1_val = IntVar()
    ae_q1_cb_2_val = IntVar()
    ae_q1_cb_3_val = IntVar()
    ae_q1_cb_4_val = IntVar()
    ae_q1_cb_5_val = IntVar()

    ae_q2_cb_1_val = IntVar()
    ae_q2_cb_2_val = IntVar()
    ae_q2_cb_3_val = IntVar()
    ae_q2_cb_4_val = IntVar()

    ae_q3_cb_1_val = IntVar()
    ae_q3_cb_2_val = IntVar()
    ae_q3_cb_3_val = IntVar()
    ae_q3_cb_4_val = IntVar()

    ae_q4_cb_1_val = IntVar()
    ae_q4_cb_2_val = IntVar()
    ae_q4_cb_3_val = IntVar()
    ae_q4_cb_4_val = IntVar()

    ae_q5_cb_1_val = IntVar()
    ae_q5_cb_2_val = IntVar()
    ae_q5_cb_3_val = IntVar()
    ae_q5_cb_4_val = IntVar()

    ae_q6_cb_1_val = IntVar()
    ae_q6_cb_2_val = IntVar()
    ae_q6_cb_3_val = IntVar()
    ae_q6_cb_4_val = IntVar()

    # checkboxes
    ae_q1_cb_1 = Checkbutton(p2, text="Strongly Agree", command=lambda: toggle(ae_q1_cb_1_val))
    ae_q1_cb_2 = Checkbutton(p2, text="Agree", command=lambda: toggle(ae_q1_cb_2_val))
    ae_q1_cb_3 = Checkbutton(p2, text="Neutral", command=lambda: toggle(ae_q1_cb_3_val))
    ae_q1_cb_4 = Checkbutton(p2, text="Disagree", command=lambda: toggle(ae_q1_cb_4_val))
    ae_q1_cb_5 = Checkbutton(p2, text="Strongly Disagree", command=lambda: toggle(ae_q1_cb_5_val))

    ae_q2_cb_1 = Checkbutton(p2, text="Very Often", command=lambda: toggle(ae_q2_cb_1_val))
    ae_q2_cb_2 = Checkbutton(p2, text="Frequently", command=lambda: toggle(ae_q2_cb_2_val))
    ae_q2_cb_3 = Checkbutton(p2, text="Seldom", command=lambda: toggle(ae_q2_cb_3_val))
    ae_q2_cb_4 = Checkbutton(p2, text="Almost Never", command=lambda: toggle(ae_q2_cb_4_val))

    ae_q3_cb_1 = Checkbutton(p2, text="Very Often", command=lambda: toggle(ae_q3_cb_1_val))
    ae_q3_cb_2 = Checkbutton(p2, text="Frequently", command=lambda: toggle(ae_q3_cb_2_val))
    ae_q3_cb_3 = Checkbutton(p2, text="Seldom", command=lambda: toggle(ae_q3_cb_3_val))
    ae_q3_cb_4 = Checkbutton(p2, text="Almost Never", command=lambda: toggle(ae_q3_cb_4_val))

    ae_q4_cb_1 = Checkbutton(p2, text="Very Often", command=lambda: toggle(ae_q4_cb_1_val))
    ae_q4_cb_2 = Checkbutton(p2, text="Frequently", command=lambda: toggle(ae_q4_cb_2_val))
    ae_q4_cb_3 = Checkbutton(p2, text="Seldom", command=lambda: toggle(ae_q4_cb_3_val))
    ae_q4_cb_4 = Checkbutton(p2, text="Almost Never", command=lambda: toggle(ae_q4_cb_4_val))

    ae_q5_cb_1 = Checkbutton(p2, text="Very Often", command=lambda: toggle(ae_q5_cb_1_val))
    ae_q5_cb_2 = Checkbutton(p2, text="Frequently", command=lambda: toggle(ae_q5_cb_2_val))
    ae_q5_cb_3 = Checkbutton(p2, text="Seldom", command=lambda: toggle(ae_q5_cb_3_val))
    ae_q5_cb_4 = Checkbutton(p2, text="Almost Never", command=lambda: toggle(ae_q5_cb_4_val))

    ae_q6_cb_1 = Checkbutton(p2, text="Very Often", command=lambda: toggle(ae_q6_cb_1_val))
    ae_q6_cb_2 = Checkbutton(p2, text="Frequently", command=lambda: toggle(ae_q6_cb_2_val))
    ae_q6_cb_3 = Checkbutton(p2, text="Seldom", command=lambda: toggle(ae_q6_cb_3_val))
    ae_q6_cb_4 = Checkbutton(p2, text="Almost Never", command=lambda: toggle(ae_q6_cb_4_val))

    # Place checkboxes
    ae_q1_cb_1.place(relx=.17, rely=.2, anchor=W)
    ae_q1_cb_2.place(relx=.34, rely=.2, anchor=W)
    ae_q1_cb_3.place(relx=.44, rely=.2, anchor=W)
    ae_q1_cb_4.place(relx=.54, rely=.2, anchor=W)
    ae_q1_cb_5.place(relx=.65, rely=.2, anchor=W)


    ae_q2_cb_1.place(relx=.17, rely=.4, anchor=W)
    ae_q2_cb_2.place(relx=.3, rely=.4, anchor=W)
    ae_q2_cb_3.place(relx=.45, rely=.4, anchor=W)
    ae_q2_cb_4.place(relx=.55, rely=.4, anchor=W)

    ae_q3_cb_1.place(relx=.17, rely=.5, anchor=W)
    ae_q3_cb_2.place(relx=.3, rely=.5, anchor=W)
    ae_q3_cb_3.place(relx=.45, rely=.5, anchor=W)
    ae_q3_cb_4.place(relx=.55, rely=.5, anchor=W)

    ae_q4_cb_1.place(relx=.17, rely=.6, anchor=W)
    ae_q4_cb_2.place(relx=.3, rely=.6, anchor=W)
    ae_q4_cb_3.place(relx=.45, rely=.6, anchor=W)
    ae_q4_cb_4.place(relx=.55, rely=.6, anchor=W)

    ae_q5_cb_1.place(relx=.17, rely=.7, anchor=W)
    ae_q5_cb_2.place(relx=.3, rely=.7, anchor=W)
    ae_q5_cb_3.place(relx=.45, rely=.7, anchor=W)
    ae_q5_cb_4.place(relx=.55, rely=.7, anchor=W)

    ae_q6_cb_1.place(relx=.17, rely=.8, anchor=W)
    ae_q6_cb_2.place(relx=.3, rely=.8, anchor=W)
    ae_q6_cb_3.place(relx=.45, rely=.8, anchor=W)
    ae_q6_cb_4.place(relx=.55, rely=.8, anchor=W)

    #
    #### Institutional Commitment page

    # Top of page text
    Label(p3, text="Institutional Commitment").place(relx=.5, rely=0, anchor=N)

    # information labels
    msg = ('Please indicate the extent to which you agree or disagree.')
    Label(p3, text=msg).place(relx=.5, rely=.1, anchor=N)

    msg = ('Please choose one of the following.')
    Label(p3, text=msg).place(relx=.5, rely=.45, anchor=N)

    msg = ('Please indicate how important each of the following was in your decision to attend OU.')
    Label(p3, text=msg).place(relx=.5, rely=.6, anchor=N)

    # labels
    q1_lbl = Label(p3, text="I am confident I made the right hcoice when choosing to attend OU:").place(relx=0, rely=.15, anchor=W)
    q2_lbl = Label(p3, text="It is important to me to graduate from OU as opposed to another university:").place(relx=0, rely=.25, anchor=W)
    q3_lbl = Label(p3, text="I plan to transfer to another college or university sometime before completing a degree at OU:").place(relx=0, rely=.35, anchor=W)
    q4_lbl = Label(p3, text="In selecting a college, OU was my _ choice:").place(relx=0, rely=.5, anchor=W)
    q5_lbl = Label(p3, text="Was not accepted at my first choice:").place(relx=0, rely=.65, anchor=W)
    q6_lbl = Label(p3, text="Could not afford my first choice:").place(relx=0, rely=.75, anchor=W)

    # checkbox variables
    ic_q1_cb_1_val = IntVar()
    ic_q1_cb_2_val = IntVar()
    ic_q1_cb_3_val = IntVar()
    ic_q1_cb_4_val = IntVar()
    ic_q1_cb_5_val = IntVar()

    ic_q2_cb_1_val = IntVar()
    ic_q2_cb_2_val = IntVar()
    ic_q2_cb_3_val = IntVar()
    ic_q2_cb_4_val = IntVar()
    ic_q2_cb_5_val = IntVar()

    ic_q3_cb_1_val = IntVar()
    ic_q3_cb_2_val = IntVar()
    ic_q3_cb_3_val = IntVar()
    ic_q3_cb_4_val = IntVar()
    ic_q3_cb_5_val = IntVar()

    ic_q4_cb_1_val = IntVar()
    ic_q4_cb_2_val = IntVar()
    ic_q4_cb_3_val = IntVar()
    ic_q4_cb_4_val = IntVar()
    ic_q4_cb_5_val = IntVar()
    ic_q4_cb_6_val = IntVar()

    ic_q5_cb_1_val = IntVar()
    ic_q5_cb_2_val = IntVar()
    ic_q5_cb_3_val = IntVar()
    ic_q5_cb_4_val = IntVar()

    ic_q6_cb_1_val = IntVar()
    ic_q6_cb_2_val = IntVar()
    ic_q6_cb_3_val = IntVar()
    ic_q6_cb_4_val = IntVar()

    # checkboxes
    ic_q1_cb_1 = Checkbutton(p3, text="Strongly Agree", command=lambda: toggle(ic_q1_cb_1_val))
    ic_q1_cb_2 = Checkbutton(p3, text="Agree", command=lambda: toggle(ic_q1_cb_2_val))
    ic_q1_cb_3 = Checkbutton(p3, text="Neutral", command=lambda: toggle(ic_q1_cb_3_val))
    ic_q1_cb_4 = Checkbutton(p3, text="Disagree", command=lambda: toggle(ic_q1_cb_4_val))
    ic_q1_cb_5 = Checkbutton(p3, text="Strongly Disagree", command=lambda: toggle(ic_q1_cb_5_val))

    ic_q2_cb_1 = Checkbutton(p3, text="Strongly Agree", command=lambda: toggle(ic_q2_cb_1_val))
    ic_q2_cb_2 = Checkbutton(p3, text="Agree", command=lambda: toggle(ic_q2_cb_2_val))
    ic_q2_cb_3 = Checkbutton(p3, text="Neutral", command=lambda: toggle(ic_q2_cb_3_val))
    ic_q2_cb_4 = Checkbutton(p3, text="Disagree", command=lambda: toggle(ic_q2_cb_4_val))
    ic_q2_cb_5 = Checkbutton(p3, text="Strongly Disagree", command=lambda: toggle(ic_q2_cb_5_val))

    ic_q3_cb_1 = Checkbutton(p3, text="Strongly Agree", command=lambda: toggle(ic_q3_cb_1_val))
    ic_q3_cb_2 = Checkbutton(p3, text="Agree", command=lambda: toggle(ic_q3_cb_2_val))
    ic_q3_cb_3 = Checkbutton(p3, text="Neutral", command=lambda: toggle(ic_q3_cb_3_val))
    ic_q3_cb_4 = Checkbutton(p3, text="Disagree", command=lambda: toggle(ic_q3_cb_4_val))
    ic_q3_cb_5 = Checkbutton(p3, text="Strongly Disagree", command=lambda: toggle(ic_q3_cb_5_val))

    ic_q4_cb_1 = Checkbutton(p3, text="1st", command=lambda: toggle(ic_q4_cb_1_val))
    ic_q4_cb_2 = Checkbutton(p3, text="2nd", command=lambda: toggle(ic_q4_cb_2_val))
    ic_q4_cb_3 = Checkbutton(p3, text="3rd", command=lambda: toggle(ic_q4_cb_3_val))
    ic_q4_cb_4 = Checkbutton(p3, text="4th", command=lambda: toggle(ic_q4_cb_4_val))
    ic_q4_cb_5 = Checkbutton(p3, text="5th", command=lambda: toggle(ic_q4_cb_5_val))
    ic_q4_cb_6 = Checkbutton(p3, text="Other", command=lambda: toggle(ic_q4_cb_6_val))

    ic_q5_cb_1 = Checkbutton(p3, text="Extremely Important", command=lambda: toggle(ic_q5_cb_1_val))
    ic_q5_cb_2 = Checkbutton(p3, text="Important", command=lambda: toggle(ic_q5_cb_2_val))
    ic_q5_cb_3 = Checkbutton(p3, text="Relatively Unimportant", command=lambda: toggle(ic_q5_cb_3_val))
    ic_q5_cb_4 = Checkbutton(p3, text="Totally Unimportant", command=lambda: toggle(ic_q5_cb_4_val))

    ic_q6_cb_1 = Checkbutton(p3, text="Extremely Important", command=lambda: toggle(ic_q6_cb_1_val))
    ic_q6_cb_2 = Checkbutton(p3, text="Important", command=lambda: toggle(ic_q6_cb_2_val))
    ic_q6_cb_3 = Checkbutton(p3, text="Relatively Unimportant", command=lambda: toggle(ic_q6_cb_3_val))
    ic_q6_cb_4 = Checkbutton(p3, text="Totally Unimportant", command=lambda: toggle(ic_q6_cb_4_val))

    # Place checkboxes
    ic_q1_cb_1.place(relx=.17, rely=.2, anchor=W)
    ic_q1_cb_2.place(relx=.34, rely=.2, anchor=W)
    ic_q1_cb_3.place(relx=.44, rely=.2, anchor=W)
    ic_q1_cb_4.place(relx=.54, rely=.2, anchor=W)
    ic_q1_cb_5.place(relx=.65, rely=.2, anchor=W)

    ic_q2_cb_1.place(relx=.17, rely=.3, anchor=W)
    ic_q2_cb_2.place(relx=.34, rely=.3, anchor=W)
    ic_q2_cb_3.place(relx=.44, rely=.3, anchor=W)
    ic_q2_cb_4.place(relx=.54, rely=.3, anchor=W)
    ic_q2_cb_5.place(relx=.65, rely=.3, anchor=W)

    ic_q3_cb_1.place(relx=.17, rely=.4, anchor=W)
    ic_q3_cb_2.place(relx=.34, rely=.4, anchor=W)
    ic_q3_cb_3.place(relx=.44, rely=.4, anchor=W)
    ic_q3_cb_4.place(relx=.54, rely=.4, anchor=W)
    ic_q3_cb_5.place(relx=.65, rely=.4, anchor=W)

    ic_q4_cb_1.place(relx=.17, rely=.55, anchor=W)
    ic_q4_cb_2.place(relx=.3, rely=.55, anchor=W)
    ic_q4_cb_3.place(relx=.45, rely=.55, anchor=W)
    ic_q4_cb_4.place(relx=.55, rely=.55, anchor=W)
    ic_q4_cb_5.place(relx=.65, rely=.55, anchor=W)
    ic_q4_cb_6.place(relx=.73, rely=.55, anchor=W)

    ic_q5_cb_1.place(relx=.17, rely=.7, anchor=W)
    ic_q5_cb_2.place(relx=.36, rely=.7, anchor=W)
    ic_q5_cb_3.place(relx=.50, rely=.7, anchor=W)
    ic_q5_cb_4.place(relx=.72, rely=.7, anchor=W)

    ic_q6_cb_1.place(relx=.17, rely=.8, anchor=W)
    ic_q6_cb_2.place(relx=.36, rely=.8, anchor=W)
    ic_q6_cb_3.place(relx=.50, rely=.8, anchor=W)
    ic_q6_cb_4.place(relx=.72, rely=.8, anchor=W)

    #
    ##### Grit page

    # Top of page text
    Label(p4, text="GRIT").place(relx=.5, rely=0, anchor=N)

    # information labels
    msg = ('Please indicate the extent to which you agree or disagree.')
    Label(p4, text=msg).place(relx=.5, rely=.1, anchor=N)

    # labels
    q1_lbl = Label(p4, text="When I encounter a setback I don't get discouraged:").place(relx=0, rely=.15, anchor=W)
    q2_lbl = Label(p4, text="I remain calm when facing difficult academic challenges:").place(relx=0, rely=.25, anchor=W)
    q3_lbl = Label(p4, text="I have accomplished a goal that took years to achieve:").place(relx=0, rely=.35, anchor=W)
    q4_lbl = Label(p4, text="Challenges motivate me:").place(relx=0, rely=.45, anchor=W)
    q5_lbl = Label(p4, text="I have overcome difficulties to conquer an important challenge:").place(relx=0, rely=.55, anchor=W)

    # checkbox variables
    grit_q1_cb_1_val = IntVar()
    grit_q1_cb_2_val = IntVar()
    grit_q1_cb_3_val = IntVar()
    grit_q1_cb_4_val = IntVar()
    grit_q1_cb_5_val = IntVar()

    grit_q2_cb_1_val = IntVar()
    grit_q2_cb_2_val = IntVar()
    grit_q2_cb_3_val = IntVar()
    grit_q2_cb_4_val = IntVar()
    grit_q2_cb_5_val = IntVar()

    grit_q3_cb_1_val = IntVar()
    grit_q3_cb_2_val = IntVar()
    grit_q3_cb_3_val = IntVar()
    grit_q3_cb_4_val = IntVar()
    grit_q3_cb_5_val = IntVar()

    grit_q4_cb_1_val = IntVar()
    grit_q4_cb_2_val = IntVar()
    grit_q4_cb_3_val = IntVar()
    grit_q4_cb_4_val = IntVar()
    grit_q4_cb_5_val = IntVar()

    grit_q5_cb_1_val = IntVar()
    grit_q5_cb_2_val = IntVar()
    grit_q5_cb_3_val = IntVar()
    grit_q5_cb_4_val = IntVar()
    grit_q5_cb_5_val = IntVar()

    # checkboxes
    grit_q1_cb_1 = Checkbutton(p4, text="Strongly Agree", command=lambda: toggle(grit_q1_cb_1_val))
    grit_q1_cb_2 = Checkbutton(p4, text="Agree", command=lambda: toggle(grit_q1_cb_2_val))
    grit_q1_cb_3 = Checkbutton(p4, text="Neutral", command=lambda: toggle(grit_q1_cb_3_val))
    grit_q1_cb_4 = Checkbutton(p4, text="Disagree", command=lambda: toggle(grit_q1_cb_4_val))
    grit_q1_cb_5 = Checkbutton(p4, text="Strongly Disagree", command=lambda: toggle(grit_q1_cb_5_val))

    grit_q2_cb_1 = Checkbutton(p4, text="Strongly Agree", command=lambda: toggle(grit_q2_cb_1_val))
    grit_q2_cb_2 = Checkbutton(p4, text="Agree", command=lambda: toggle(grit_q2_cb_2_val))
    grit_q2_cb_3 = Checkbutton(p4, text="Neutral", command=lambda: toggle(grit_q2_cb_3_val))
    grit_q2_cb_4 = Checkbutton(p4, text="Disagree", command=lambda: toggle(grit_q2_cb_4_val))
    grit_q2_cb_5 = Checkbutton(p4, text="Strongly Disagree", command=lambda: toggle(grit_q2_cb_5_val))

    grit_q3_cb_1 = Checkbutton(p4, text="Strongly Agree", command=lambda: toggle(grit_q3_cb_1_val))
    grit_q3_cb_2 = Checkbutton(p4, text="Agree", command=lambda: toggle(grit_q3_cb_2_val))
    grit_q3_cb_3 = Checkbutton(p4, text="Neutral", command=lambda: toggle(grit_q3_cb_3_val))
    grit_q3_cb_4 = Checkbutton(p4, text="Disagree", command=lambda: toggle(grit_q3_cb_4_val))
    grit_q3_cb_5 = Checkbutton(p4, text="Strongly Disagree", command=lambda: toggle(grit_q3_cb_5_val))

    grit_q4_cb_1 = Checkbutton(p4, text="Strongly Agree", command=lambda: toggle(grit_q4_cb_1_val))
    grit_q4_cb_2 = Checkbutton(p4, text="Agree", command=lambda: toggle(grit_q4_cb_2_val))
    grit_q4_cb_3 = Checkbutton(p4, text="Neutral", command=lambda: toggle(grit_q4_cb_3_val))
    grit_q4_cb_4 = Checkbutton(p4, text="Disagree", command=lambda: toggle(grit_q4_cb_4_val))
    grit_q4_cb_5 = Checkbutton(p4, text="Strongly Disagree", command=lambda: toggle(grit_q4_cb_5_val))

    grit_q5_cb_1 = Checkbutton(p4, text="Strongly Agree", command=lambda: toggle(grit_q5_cb_1_val))
    grit_q5_cb_2 = Checkbutton(p4, text="Agree", command=lambda: toggle(grit_q5_cb_2_val))
    grit_q5_cb_3 = Checkbutton(p4, text="Neutral", command=lambda: toggle(grit_q5_cb_3_val))
    grit_q5_cb_4 = Checkbutton(p4, text="Disagree", command=lambda: toggle(grit_q5_cb_4_val))
    grit_q5_cb_5 = Checkbutton(p4, text="Strongly Disagree", command=lambda: toggle(grit_q5_cb_5_val))

    # Place checkboxes
    grit_q1_cb_1.place(relx=.17, rely=.2, anchor=W)
    grit_q1_cb_2.place(relx=.34, rely=.2, anchor=W)
    grit_q1_cb_3.place(relx=.44, rely=.2, anchor=W)
    grit_q1_cb_4.place(relx=.54, rely=.2, anchor=W)
    grit_q1_cb_5.place(relx=.65, rely=.2, anchor=W)

    grit_q2_cb_1.place(relx=.17, rely=.3, anchor=W)
    grit_q2_cb_2.place(relx=.34, rely=.3, anchor=W)
    grit_q2_cb_3.place(relx=.44, rely=.3, anchor=W)
    grit_q2_cb_4.place(relx=.54, rely=.3, anchor=W)
    grit_q2_cb_5.place(relx=.65, rely=.3, anchor=W)

    grit_q3_cb_1.place(relx=.17, rely=.4, anchor=W)
    grit_q3_cb_2.place(relx=.34, rely=.4, anchor=W)
    grit_q3_cb_3.place(relx=.44, rely=.4, anchor=W)
    grit_q3_cb_4.place(relx=.54, rely=.4, anchor=W)
    grit_q3_cb_5.place(relx=.65, rely=.4, anchor=W)

    grit_q4_cb_1.place(relx=.17, rely=.5, anchor=W)
    grit_q4_cb_2.place(relx=.34, rely=.5, anchor=W)
    grit_q4_cb_3.place(relx=.44, rely=.5, anchor=W)
    grit_q4_cb_4.place(relx=.54, rely=.5, anchor=W)
    grit_q4_cb_5.place(relx=.65, rely=.5, anchor=W)

    grit_q5_cb_1.place(relx=.17, rely=.6, anchor=W)
    grit_q5_cb_2.place(relx=.34, rely=.6, anchor=W)
    grit_q5_cb_3.place(relx=.44, rely=.6, anchor=W)
    grit_q5_cb_4.place(relx=.54, rely=.6, anchor=W)
    grit_q5_cb_5.place(relx=.65, rely=.6, anchor=W)

    # Add checkboxes to the dictionary to be monitored later
    fc1 = [fc_q1_cb_1_val, fc_q1_cb_2_val, fc_q1_cb_3_val, fc_q1_cb_4_val, fc_q1_cb_5_val]
    fc2 = [fc_q2_cb_1_val, fc_q2_cb_2_val, fc_q2_cb_3_val, fc_q2_cb_4_val, fc_q2_cb_5_val]
    fc3 = [fc_q3_cb_1_val, fc_q3_cb_2_val, fc_q3_cb_3_val, fc_q3_cb_4_val, fc_q3_cb_5_val]
    fc4 = [fc_q4_cb_1_val, fc_q4_cb_2_val, fc_q4_cb_3_val, fc_q4_cb_4_val]
    
    ae1 = [ae_q1_cb_1_val, ae_q1_cb_2_val, ae_q1_cb_3_val, ae_q1_cb_4_val, ae_q1_cb_5_val]
    ae2 = [ae_q2_cb_1_val, ae_q2_cb_2_val, ae_q2_cb_3_val, ae_q2_cb_4_val]
    ae3 = [ae_q3_cb_1_val, ae_q3_cb_2_val, ae_q3_cb_3_val, ae_q3_cb_4_val]
    ae4 = [ae_q4_cb_1_val, ae_q4_cb_2_val, ae_q4_cb_3_val, ae_q4_cb_4_val]
    ae5 = [ae_q5_cb_1_val, ae_q5_cb_2_val, ae_q5_cb_3_val, ae_q5_cb_4_val]
    ae6 = [ae_q6_cb_1_val, ae_q6_cb_2_val, ae_q6_cb_3_val, ae_q6_cb_4_val]

    ic1 = [ic_q1_cb_1_val, ic_q1_cb_2_val, ic_q1_cb_3_val, ic_q1_cb_4_val, ic_q1_cb_5_val]
    ic2 = [ic_q2_cb_1_val, ic_q2_cb_2_val, ic_q2_cb_3_val, ic_q2_cb_4_val, ic_q2_cb_5_val]
    ic3 = [ic_q3_cb_1_val, ic_q3_cb_2_val, ic_q3_cb_3_val, ic_q3_cb_4_val, ic_q3_cb_5_val]
    ic4 = [ic_q4_cb_1_val, ic_q4_cb_2_val, ic_q4_cb_3_val, ic_q4_cb_4_val, ic_q4_cb_5_val, ic_q4_cb_6_val]
    ic5 = [ic_q5_cb_1_val, ic_q5_cb_2_val, ic_q5_cb_3_val, ic_q5_cb_4_val]
    ic6 = [ic_q6_cb_1_val, ic_q6_cb_2_val, ic_q6_cb_3_val, ic_q6_cb_4_val]

    grit1 = [grit_q1_cb_1_val, grit_q1_cb_2_val, grit_q1_cb_3_val, grit_q1_cb_4_val, grit_q1_cb_5_val]
    grit2 = [grit_q2_cb_1_val, grit_q2_cb_2_val, grit_q2_cb_3_val, grit_q2_cb_4_val, grit_q2_cb_5_val]
    grit3 = [grit_q3_cb_1_val, grit_q3_cb_2_val, grit_q3_cb_3_val, grit_q3_cb_4_val, grit_q3_cb_5_val]
    grit4 = [grit_q4_cb_1_val, grit_q4_cb_2_val, grit_q4_cb_3_val, grit_q4_cb_4_val, grit_q4_cb_5_val]
    grit5 = [grit_q5_cb_1_val, grit_q5_cb_2_val, grit_q5_cb_3_val, grit_q5_cb_4_val, grit_q5_cb_5_val]

    checks['fc'] =   [fc1, fc2, fc3, fc4]
    checks['ae'] =   [ae1, ae2, ae3, ae4, ae5, ae6]
    checks['ic'] =   [ic1, ic2, ic3, ic4, ic5, ic6]
    checks['grit'] = [grit1, grit2, grit3, grit4, grit5]

    #
    # Add pages to page list
    pages.append(p1)
    pages.append(p2)
    pages.append(p3)
    pages.append(p4)

    return pages, checks

def raise_next(p):
    p.increment()
    p.raise_frame()

def raise_prev(p):
    p.decrement()
    p.raise_frame()

##### Views
def run_open_dialog(main):
    open = Toplevel(main)
    msg = ('Welcome! \n \n'
           'This application was created by Koby Pascual, Yutian Tang, Melie Lewis, and Timothy Burt. \n \n'
           'The intention of this project is to use data mining techniques to predict freshman student retention at the University of Oklahoma.\n\n'
           'If you are familiar with this application, continue. Otherwise, please browse the brief tutorial.')

    Message(open, text=msg).pack()
    Button(open, text="Okay", command=lambda: open.destroy()).pack()
    open.lift(main)

def run_tutorial_view():
    # Create tutorial view
    tut = Toplevel()

    # Create tutorial pages
    pages = create_tutorial_pages(tut)

    # Raise default screen
    pages.raise_frame()

    # Button frame
    but_frame = Frame(tut)
    but_frame.grid(row=0,column=0,sticky='news')

    # Add buttons
    prev = Button(but_frame, text="Previous", command=lambda: raise_prev(pages)).grid(row=0,column=0)
    done = Button(but_frame, text="Done",     command=lambda: tut.destroy()).grid(row=0,column=1)
    next = Button(but_frame, text="Next",     command=lambda: raise_next(pages)).grid(row=0,column=2)


    # Configurations
    tut.title("Tutorial")
    tut.minsize(width=500, height=250)

def run_entry_view():
    entry = Toplevel()

    # Get entry page
    entry_page, e_fields = create_entry_page(entry)

    # Get survey pages
    survey_pages, e_checks = create_survey_pages(entry)

    # Create pointer list and append all of the pages to it
    pages = Pointer_List.pointer_list()
    pages.add(entry_page)
    [pages.add(p) for p in survey_pages]

    # Raise the first page
    pages.raise_frame()

    # Button frame
    but_f = Frame(entry)
    but_f.grid(row=0,column=0,sticky='news')

    # Add buttons
    prev = Button(but_f, text="Previous", command=lambda: raise_prev(pages)).grid(row=0,column=0)
    submit = Button(but_f, text="Submit",     command=lambda: submit_entry(entry, e_fields, e_checks)).grid(row=0,column=1)
    next = Button(but_f, text="Next",     command=lambda: raise_next(pages)).grid(row=0,column=2)

    # Configurations
    entry.title("Add New Student Data")
    entry.minsize(width=800,height=500)

def run_output_view(result):
    output = Toplevel()

    # main frame
    result_frame = Frame(output)
    result_frame.grid(row=1, column=0, sticky='news')

    if result == True:
        msg = ("Success! Based on our algorithms it seems like this student is bound for success at OU. \n \n"
               "Retention is highly probable. Good luck and stay focused!")
        title = ("Classification results: Not Retained")
    elif result == False:
        msg = ("Unfortunately, the result we have obtained from our algorithm leans toward this student"
               " leaving school after their freshman year.\n\nMaybe this student would like to try a different"
               " combination of courses, a lighter workload, or even perhaps a new major? \n \n")
        title = ("Classification results: Not Retained")

    Message(output, text=msg).pack(side=BOTTOM)

    # Add buttons
    done = Button(output, text="Done", command=lambda: output_dialog(output)).pack(side=TOP)

    # configurations
    output.title(title)

def run_main_view():
    # create the main view
    main = Tk()

    # Run the open dialog
    run_open_dialog(main)

    # Add image to background
    bck_ground_image = ImageTk.PhotoImage(file='dm_image.png')
    bck_ground_label = Label(main, image=bck_ground_image)
    bck_ground_label.place(x=0,y=0,relwidth=1,relheight=1)

    # add menubar to main view
    menubar = Menu(main)

    # Add menu items to the main view
    tutorialmenu = Menu(menubar, tearoff = 0) # this one is empty for now
    tutorialmenu.add_command(label="Start",command=run_tutorial_view)
    menubar.add_cascade(label="Tutorial", menu=tutorialmenu)

    # Create mains buttons
    input_new = Button(main, text="Add New Student", command=run_entry_view)
    input_new.pack(side=BOTTOM)
    #test_r = Button(main, text="test r", command=lambda: run_r(10))
    #test_r.pack(side=LEFT)

    # Configurations
    main.title("Predicting Student Retention Using Enrollment Data")
    main.config(menu=menubar)
    main.minsize(width=500,height=500)
    main.mainloop()

###################
# Main Program
###################
run_main_view()