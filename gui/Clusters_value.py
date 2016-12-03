import random

class Cluster_value:

    def __init__(self, clust_val):
        self.centers = {}
        self.set_clusters(clust_val)

    def find_closest(self,p):
        max = 0
        id = -1
        dict_count = 0

        for key, value in self.centers.iteritems():
            tmp = self.compare(p,value)
            dict_count += 1

            if tmp > max:
                max = tmp
                id = key

        if id == -1:
            id = random.randint(0,dict_count-1)
        return str(id)

    def compare(self,p,value):
        count = 0
        for i in p.courses:
            for j in value:
                if i == j:
                    count += 1

        return count
    
    def set_clusters(self, which):
        # 0 is for k_modes clusters
        if which == 0:
            self.centers[0] = ['CHEM1315', 'ENGL1113', 'MATH1523', 'UCOL1002', 'CHEM1315B', '.', '.']
            self.centers[1] = ['ENGL1113', 'MATH1503', 'UCOL1002', 'BIOL1114', 'BIOL1114', 'BIOL1121', '.', '.']
            self.centers[2] = ['CHEM1315', 'MUNM1113', 'PSY 1113', 'ENGR1411', 'UCOL1002', 'CHEM1315B', '.']
            self.centers[3] = ['ENGL1213', 'MATH1523', 'MUNM1113', 'PSY 1113', 'UCOL1002', '.', '.']
            self.centers[4] = ['AHS 1400', 'MATH1643', 'PSY 1113', 'UCOL1002', 'BIOL1114', 'BIOL1121', '.']
            self.centers[5] = ['B AD1001', 'COMM1113', 'MATH1643', 'SOC 1113', 'ENGL1113', '.', '.']
            self.centers[6] = ['COMM1113', 'ECON1123', 'ENGL1113', 'MATH1643', '.', '.', '.']
            self.centers[7] = ['ENGL1113', 'AHS 1400', 'MATH1503', 'UCOL1002', 'UCOL1002', 'BIOL1121', '.']
            self.centers[8] = ['ENGL1113', 'SPAN1115', 'PSY 1113', 'UCOL1002', '.', '.', '.']
            self.centers[9] = ['CHEM1315', 'ENGL1113', 'ENGR1411', 'MATH1914', 'MATH1914B', 'CHEM1315B', 'ENGR1411B']
            self.centers[10] =['MATH1503', 'UCOL1002', 'BIOL1114', 'BIOL1121', 'PSY 1113', '.', '.']
            