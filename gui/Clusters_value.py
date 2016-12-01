
class Cluster_value:

    def __init__(self, clust):
        self.centers = {}

        for c in range(len(clust)):
            self.centers[c] = clust[c]

    def find_closest(self,p):
        max = 0
        id = -1

        for key, value in self.centers.iteritems():
            tmp = self.compare(p,value)

            if tmp > max:
                max = tmp
                id = key

        return key

    def compare(self,p,value):
        count = 0
        for i in p.courses:
            for j in value:
                if i.strip() == j.strip():
                    count += 1

        return count