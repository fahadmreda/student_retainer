###################
# Imports
###################
# External files
from Tkinter import *
import tkMessageBox
from PIL import Image,ImageTk

# Homemade files
import Point
import Pointer_List

###################
# Globals
###################

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

def check_entry(entries):
    for key, value in entries.iteritems():
        if not value.get():
            return False
    return True

def clear_entry(entries, checks):
    for key, value in entries.iteritems():
        value.delete(0,END)

    for key, value in checks.iteritems():
        value.deselect()

def submit_entry(entry, entries, checks):
    # TODO - Error checking
    if check_entry(entries):
        new_point = Point.Point(entries, checks)
        entry.destroy()
    else:
        tkMessageBox.showerror(message="Invalid Entry")

def create_tutorial_pages(tut):
    pages = Pointer_List.pointer_list()

    p1 = Frame(tut)
    p2 = Frame(tut)
    p3 = Frame(tut)
    p4 = Frame(tut)

    p1.grid(row=0, column=0, sticky='news')
    p2.grid(row=0, column=0, sticky='news')
    p3.grid(row=0, column=0, sticky='news')
    p4.grid(row=0, column=0, sticky='news')

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

    Label(p1, text=msg).pack()

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
    msg = ('Now, fill out each entry with the appropriate data. If no data is available, input NaN. No field can be empty. \n'
            'Check boxes do not need to be checked. Only check the boxes which are appropriate. \n'
            'Click "Submit and Classify"'
            'If you decide to start over, click "Clear" and all fields will be reset')
    Message(p3, text=msg).grid(row=0,column=1)

    bck_ground_image = ImageTk.PhotoImage(file='input_tut.png')
    bck_ground_label = Label(p3, image=bck_ground_image)
    bck_ground_label.grid(row=2,column=1)
    bck_ground_label.image = bck_ground_image

    #####
    ##### Page 4
    msg = ('Notice: If you fill out an entry with an invalid type an error message will occur. \n'
           'Simply click "ok" and continue filling out the form.')
    Label(p4, text=msg).grid(row=0,column=1)

    bck_ground_image = ImageTk.PhotoImage(file='incorrect_tut.png')
    bck_ground_label = Label(p4, image=bck_ground_image)
    bck_ground_label.grid(row=2,column=1)
    bck_ground_label.image = bck_ground_image

    # Add the pages to the pointer list
    pages.add(p1)
    pages.add(p2)
    pages.add(p3)
    pages.add(p4)

    return pages

def raise_next(p):
    p.increment()
    p.raise_frame()

def raise_prev(p):
    p.decrement()
    p.raise_frame()

##### View
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


    # Add buttons
    prev = Button(tut, text="Previous", command=lambda: raise_prev(pages)).place(relx=.25, rely=.95, anchor=CENTER)
    done = Button(tut, text="Done",     command=lambda: tut.destroy()).place(relx=.5, rely=.95, anchor=CENTER)
    next = Button(tut, text="Next",     command=lambda: raise_next(pages)).place(relx=.75, rely=.95, anchor=CENTER)

    # Configurations
    tut.title("Tutorial")
    tut.minsize(width=500, height=900)

def run_entry_view():
    entry = Tk()

    # List of all the entry fields and checkbox fields
    entries = {}
    checks = {}

    # Add all of the labels needed
    act_comp_lbl =              Label(entry, text="ACT Comp").grid(row=0, column=0)
    act_english_lbl =           Label(entry, text="ACT English").grid(row=1, column=0)
    act_math_lbl =              Label(entry, text="ACT Math").grid(row=2, column=0)
    act_reading_lbl =           Label(entry, text="ACT Reading").grid(row=3, column=0)
    act_science_lbl =           Label(entry, text="ACT Science").grid(row=4, column=0)
    act_sat_conv_lbl =          Label(entry, text="ACT-SAT Conversion").grid(row=5, column=0)
    ap_hours_lbl =              Label(entry, text="AP Hours").grid(row=6, column=0)
    credits_attempted_lbl =     Label(entry, text="Credits Attempted").grid(row=7, column=0)
    ret_gpa_lbl =               Label(entry, text="Ret GPA").grid(row=8, column=0)
    hs_gpa_lbl =                Label(entry, text="HS GPA").grid(row=9, column=0)
    trig_lbl =                  Label(entry, text="Trig").grid(row=10, column=0)
    alg_1_lbl =                 Label(entry, text="Alg I").grid(row=11, column=0)
    alg_2_lbl =                 Label(entry, text="Alg II").grid(row=12, column=0)
    alg_coll_lbl =              Label(entry, text="Coll Alg").grid(row=13, column=0)
    geometry_lbl =              Label(entry, text="Geometry").grid(row=14, column=0)
    pre_calc_lbl =              Label(entry, text="Pre-Calc").grid(row=15, column=0)
    stats_lbl =                 Label(entry, text="Stats").grid(row=16, column=0)
    math_senior_lbl =           Label(entry, text="Math Senior").grid(row=17, column=0)
    fc_lbl =                    Label(entry, text="FC").grid(row=18, column=0)
    ae_lbl =                    Label(entry, text="AE").grid(row=0, column=2)
    ic_lbl =                    Label(entry, text="IC").grid(row=1, column=2)
    grit_lbl =                  Label(entry, text="GRIT").grid(row=2, column=2)
    here_lbl =                  Label(entry, text="Here").grid(row=3, column=2)
    cohort_ou_term_lbl =        Label(entry, text="Cohort OU Term").grid(row=4, column=2)
    t_course_1_lbl =            Label(entry, text="Title: Course 1").grid(row=5, column=2)
    t_course_2_lbl =            Label(entry, text="Title: Course 2").grid(row=6, column=2)
    t_course_3_lbl =            Label(entry, text="Title: Course 3").grid(row=7, column=2)
    t_course_4_lbl =            Label(entry, text="Title: Course 4").grid(row=8, column=2)
    t_course_5_lbl =            Label(entry, text="Title: Course 5").grid(row=9, column=2)
    t_course_6_lbl =            Label(entry, text="Title: Course 6").grid(row=10, column=2)
    t_course_7_lbl =            Label(entry, text="Title: Course 7").grid(row=11, column=2)
    g_course_1_lbl =            Label(entry, text="Grade: Course 1").grid(row=12, column=2)
    g_course_2_lbl =            Label(entry, text="Grade: Course 2").grid(row=13, column=2)
    g_course_3_lbl =            Label(entry, text="Grade: Course 3").grid(row=14, column=2)
    g_course_4_lbl =            Label(entry, text="Grade: Course 4").grid(row=15, column=2)
    g_course_5_lbl =            Label(entry, text="Grade: Course 5").grid(row=16, column=2)
    g_course_6_lbl =            Label(entry, text="Grade: Course 6").grid(row=17, column=2)
    g_course_7_lbl =            Label(entry, text="Grade: Course 7").grid(row=18, column=2)
    major_lbl =                 Label(entry, text="Major").grid(row=0, column=4)

    # Add entry fields
    act_comp_entry =            Entry(entry, bd=5)
    act_english_entry =         Entry(entry, bd=5)
    act_math_entry =            Entry(entry, bd=5)
    act_reading_entry =         Entry(entry, bd=5)
    act_science_entry =         Entry(entry, bd=5)
    act_sat_conv_entry =        Entry(entry, bd=5)
    ap_hours_entry =            Entry(entry, bd=5)
    credits_attempted_entry =   Entry(entry, bd=5)
    ret_gpa_entry =             Entry(entry, bd=5)
    hs_gpa_entry =              Entry(entry, bd=5)
    trig_entry =                Entry(entry, bd=5)
    alg_1_entry =               Entry(entry, bd=5)
    alg_2_entry =               Entry(entry, bd=5)
    alg_coll_entry =            Entry(entry, bd=5)
    geometry_entry =            Entry(entry, bd=5)
    pre_calc_entry =            Entry(entry, bd=5)
    stats_entry =               Entry(entry, bd=5)
    math_senior_entry =         Entry(entry, bd=5)
    fc_entry =                  Entry(entry, bd=5)
    ae_entry =                  Entry(entry, bd=5)
    ic_entry =                  Entry(entry, bd=5)
    grit_entry =                Entry(entry, bd=5)
    here_entry =                Entry(entry, bd=5)
    cohort_ou_term_entry =      Entry(entry, bd=5)
    t_course_1_entry =          Entry(entry, bd=5)
    t_course_2_entry =          Entry(entry, bd=5)
    t_course_3_entry =          Entry(entry, bd=5)
    t_course_4_entry =          Entry(entry, bd=5)
    t_course_5_entry =          Entry(entry, bd=5)
    t_course_6_entry =          Entry(entry, bd=5)
    t_course_7_entry =          Entry(entry, bd=5)
    g_course_1_entry =          Entry(entry, bd=5)
    g_course_2_entry =          Entry(entry, bd=5)
    g_course_3_entry =          Entry(entry, bd=5)
    g_course_4_entry =          Entry(entry, bd=5)
    g_course_5_entry =          Entry(entry, bd=5)
    g_course_6_entry =          Entry(entry, bd=5)
    g_course_7_entry =          Entry(entry, bd=5)
    major_entry =               Entry(entry, bd=5)

    # Create checkbox variables
    o_course_1_val = IntVar()
    o_course_2_val = IntVar()
    o_course_3_val = IntVar()
    o_course_4_val = IntVar()
    o_course_5_val = IntVar()
    o_course_6_val = IntVar()
    o_course_7_val = IntVar()

    # Add checkboxes
    o_course_1 =                Checkbutton(entry, text="Online: Course 1", variable=o_course_1_val, command=lambda: toggle(o_course_1_val))
    o_course_2 =                Checkbutton(entry, text="Online: Course 2", variable=o_course_2_val, command=lambda: toggle(o_course_2_val))
    o_course_3 =                Checkbutton(entry, text="Online: Course 3", variable=o_course_3_val, command=lambda: toggle(o_course_3_val))
    o_course_4 =                Checkbutton(entry, text="Online: Course 4", variable=o_course_4_val, command=lambda: toggle(o_course_4_val))
    o_course_5 =                Checkbutton(entry, text="Online: Course 5", variable=o_course_5_val, command=lambda: toggle(o_course_5_val))
    o_course_6 =                Checkbutton(entry, text="Online: Course 6", variable=o_course_6_val, command=lambda: toggle(o_course_6_val))
    o_course_7 =                Checkbutton(entry, text="Online: Course 7", variable=o_course_7_val, command=lambda: toggle(o_course_7_val))

    # Place entry & checkbox fields in appropriate locations
    act_comp_entry.grid(row=0, column=1)
    act_english_entry.grid(row=1, column=1)
    act_math_entry.grid(row=2, column=1)
    act_reading_entry.grid(row=3, column=1)
    act_science_entry.grid(row=4, column=1)
    act_sat_conv_entry.grid(row=5, column=1)
    ap_hours_entry.grid(row=6, column=1)
    credits_attempted_entry.grid(row=7, column=1)
    ret_gpa_entry.grid(row=8, column=1)
    hs_gpa_entry.grid(row=9, column=1)
    trig_entry.grid(row=10, column=1)
    alg_1_entry.grid(row=11, column=1)
    alg_2_entry.grid(row=12, column=1)
    alg_coll_entry.grid(row=13, column=1)
    geometry_entry.grid(row=14, column=1)
    pre_calc_entry.grid(row=15, column=1)
    stats_entry.grid(row=16, column=1)
    math_senior_entry.grid(row=17, column=1)
    fc_entry.grid(row=18, column=1)
    ae_entry.grid(row=0, column=3)
    ic_entry.grid(row=1, column=3)
    grit_entry.grid(row=2, column=3)
    here_entry.grid(row=3, column=3)
    cohort_ou_term_entry.grid(row=4, column=3)
    t_course_1_entry.grid(row=5, column=3)
    t_course_2_entry.grid(row=6, column=3)
    t_course_3_entry.grid(row=7, column=3)
    t_course_4_entry.grid(row=8, column=3)
    t_course_5_entry.grid(row=9, column=3)
    t_course_6_entry.grid(row=10, column=3)
    t_course_7_entry.grid(row=11, column=3)
    g_course_1_entry.grid(row=12, column=3)
    g_course_2_entry.grid(row=13, column=3)
    g_course_3_entry.grid(row=14, column=3)
    g_course_4_entry.grid(row=15, column=3)
    g_course_5_entry.grid(row=16, column=3)
    g_course_6_entry.grid(row=17, column=3)
    g_course_7_entry.grid(row=18, column=3)
    major_entry.grid(row=0, column=5)
    o_course_1.grid(row=1, column=5)
    o_course_2.grid(row=2, column=5)
    o_course_3.grid(row=3, column=5)
    o_course_4.grid(row=4, column=5)
    o_course_5.grid(row=5, column=5)
    o_course_6.grid(row=6, column=5)
    o_course_7.grid(row=7, column=5)

    # Add entries to the lists
    entries['act_comp_entry']           = act_comp_entry
    entries['act_english_entry']        = act_english_entry
    entries['act_math_entry']           = act_math_entry
    entries['act_reading_entry']        = act_reading_entry
    entries['act_science_entry']        = act_science_entry
    entries['act_sat_conv_entry']       = act_sat_conv_entry
    entries['ap_hours_entry']           = ap_hours_entry
    entries['credits_attempted_entry']  = credits_attempted_entry
    entries['ret_gpa_entry']            = ret_gpa_entry
    entries['hs_gpa_entry']             = hs_gpa_entry
    entries['trig_entry']               = trig_entry
    entries['alg_1_entry']              = alg_1_entry
    entries['alg_2_entry']              = alg_2_entry
    entries['alg_coll_entry']           = alg_coll_entry
    entries['geometry_entry']           = geometry_entry
    entries['pre_calc_entry']           = pre_calc_entry
    entries['stats_entry']              = stats_entry
    entries['math_senior_entry']        = math_senior_entry
    entries['fc_entry']                 = fc_entry
    entries['ae_entry']                 = ae_entry
    entries['ic_entry']                 = ic_entry
    entries['grit_entry']               = grit_entry
    entries['here_entry']               = here_entry
    entries['cohort_ou_term_entry']     = cohort_ou_term_entry
    entries['t_course_1_entry']         = t_course_1_entry
    entries['t_course_2_entry']         = t_course_2_entry
    entries['t_course_3_entry']         = t_course_3_entry
    entries['t_course_4_entry']         = t_course_4_entry
    entries['t_course_5_entry']         = t_course_5_entry
    entries['t_course_6_entry']         = t_course_6_entry
    entries['t_course_7_entry']         = t_course_7_entry
    entries['g_course_1_entry']         = g_course_1_entry
    entries['g_course_2_entry']         = g_course_2_entry
    entries['g_course_3_entry']         = g_course_3_entry
    entries['g_course_4_entry']         = g_course_4_entry
    entries['g_course_5_entry']         = g_course_5_entry
    entries['g_course_6_entry']         = g_course_6_entry
    entries['g_course_7_entry']         = g_course_7_entry
    entries['major_entry']              = major_entry

    checks['o_course_1']                = o_course_1_val
    checks['o_course_2']                = o_course_2_val
    checks['o_course_3']                = o_course_3_val
    checks['o_course_4']                = o_course_4_val
    checks['o_course_5']                = o_course_5_val
    checks['o_course_6']                = o_course_6_val
    checks['o_course_7']                = o_course_7_val

    # Add Buttons
    submit_btn = Button(entry, text="Submit and Classify", command=lambda: submit_entry(entry, entries, checks)).grid(row=19, column=1)
    clear_btn = Button(entry, text="Clear", command=lambda: clear_entry(entries, checks)).grid(row=19, column=3)

    # Configurations
    entry.title("Add New Student Data")

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

    # Configurations
    main.title("Predicting Student Retention Using Enrollment Data")
    main.config(menu=menubar)
    main.minsize(width=500,height=500)
    main.mainloop()

###################
# Main Program
###################
run_main_view()