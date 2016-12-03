
class Point:
    def __init__(self, entries, checks):
        self.act_sat_conv =         entries['act_sat_conv_entry'].get()
        self.ap_hours =             entries['ap_hours_entry'].get()
        self.hs_gpa =               entries['hs_gpa_entry'].get()
        self.trig =                 entries['trig_entry'].get()
        self.alg_1 =                entries['alg_1_entry'].get()
        self.alg_2 =                entries['alg_2_entry'].get()
        self.alg_coll =             entries['alg_coll_entry'].get()
        self.geometry =             entries['geometry_entry'].get()
        self.pre_calc =             entries['pre_calc_entry'].get()
        self.stats =                entries['stats_entry'].get()
        self.math_senior =          entries['math_senior_entry'].get()

        self.t_course_1 =           entries['t_course_1_entry'].get()
        self.t_course_2 =           entries['t_course_2_entry'].get()
        self.t_course_3 =           entries['t_course_3_entry'].get()
        self.t_course_4 =           entries['t_course_4_entry'].get()
        self.t_course_5 =           entries['t_course_5_entry'].get()
        self.t_course_6 =           entries['t_course_6_entry'].get()
        self.t_course_7 =           entries['t_course_7_entry'].get()
        self.courses = [self.t_course_1,self.t_course_2,self.t_course_3,self.t_course_4,self.t_course_5,self.t_course_6, self.t_course_7]
        self.cluster_name = None


        self.fc =                   self.calculate_survey(checks['fc'], [2,4])
        self.ae =                   self.calculate_survey(checks['ae'], [])
        self.ic =                   self.calculate_survey(checks['ic'], [1,2,4])
        self.grit =                 self.calculate_survey(checks['grit'], [])

        self.major =                entries['major_entry'].get()

        self.info_vector = [self.act_sat_conv, self.ap_hours, self.hs_gpa, self.trig, self.alg_1, self.alg_2, self.alg_coll,
                       self.geometry, self.pre_calc, self.stats, self.math_senior, self.fc, self.ae, self.ic, self.grit,
                       self.major, self.cluster_name]

    def calculate_survey(self, check, invert):
        sum = 0
        for i in range(len(check)):
            question = check[i]
            for j in range(len(question)):
                answer = question[j]
                if answer.get() == 1:
                    if i+1 in invert:
                        if len(question) == 6:
                            sum = sum + (len(question) - (j+1))
                        else:
                            sum = sum + (len(question)+1) - (j+1)
                    else:
                        sum = sum + j+1

        return float(sum) / len(check)