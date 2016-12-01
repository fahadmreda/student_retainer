
class Point:
    def __init__(self, entries, checks):
        self.act_comp =             entries['act_comp_entry']
        self.act_english =          entries['act_english_entry']
        self.act_math =             entries['act_math_entry']
        self.act_reading =          entries['act_reading_entry']
        self.act_science =          entries['act_science_entry']
        self.act_sat_conv =         entries['act_sat_conv_entry']
        self.ap_hours =             entries['ap_hours_entry']
        self.credits_attempted =    entries['credits_attempted_entry']

        self.ret_gpa =              entries['ret_gpa_entry']
        self.hs_gpa =               entries['hs_gpa_entry']
        self.trig =                 entries['trig_entry']
        self.alg_1 =                entries['alg_1_entry']
        self.alg_2 =                entries['alg_2_entry']
        self.alg_coll =             entries['alg_coll_entry']
        self.geometry =             entries['geometry_entry']
        self.pre_calc =             entries['pre_calc_entry']
        self.stats =                entries['stats_entry']
        self.math_senior =          entries['math_senior_entry']
        self.fc =                   entries['fc_entry']
        self.ae =                   entries['ae_entry']
        self.ic =                   entries['ic_entry']
        self.grit =                 entries['grit_entry']
        self.cohort_ou_term =       entries['cohort_ou_term_entry']

        self.t_course_1 =           entries['t_course_1_entry']
        self.t_course_2 =           entries['t_course_2_entry']
        self.t_course_3 =           entries['t_course_3_entry']
        self.t_course_4 =           entries['t_course_4_entry']
        self.t_course_5 =           entries['t_course_5_entry']
        self.t_course_6 =           entries['t_course_6_entry']
        self.t_course_7 =           entries['t_course_7_entry']
        self.g_course_1 =           entries['g_course_1_entry']
        self.g_course_2 =           entries['g_course_2_entry']
        self.g_course_3 =           entries['g_course_3_entry']
        self.g_course_4 =           entries['g_course_4_entry']
        self.g_course_5 =           entries['g_course_5_entry']
        self.g_course_6 =           entries['g_course_6_entry']
        self.g_course_7 =           entries['g_course_7_entry']

        self.major =                entries['major_entry']

        self.o_course_1 =           checks['o_course_1'].get()
        self.o_course_2 =           checks['o_course_2'].get()
        self.o_course_3 =           checks['o_course_3'].get()
        self.o_course_4 =           checks['o_course_4'].get()
        self.o_course_5 =           checks['o_course_5'].get()
        self.o_course_6 =           checks['o_course_6'].get()
        self.o_course_7 =           checks['o_course_7'].get()

        self.cluster_name = None
        self.courses = [self.t_course_1,self.t_course_2,self.t_course_3,self.t_course_4,self.t_course_5,self.t_course_6, self.t_course_7]