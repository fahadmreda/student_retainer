# Script to generate knee plot from k-modes
# Tim Burt
# CS5593 project

import csv
import os
import matplotlib.pyplot as plt
import numpy as np

import kmodes

# options
max_clusters = 30
save_dir = 'examples'
# initialize variables
classes_dict = {}
class_counter = 0
line_counter = 0
dup_class_counter = 0
data_filename = 'cleaned_data.csv'
clean_data_filename = 'cleaned_data_nodups.csv'  # written WITHOUT any duplicate records in a class
#
classes_dict['.'] = 0  # force that as unknown class
os.chdir(save_dir)
file = open(data_filename)
row_count = len(file.readlines())
colm_count = 7
data_sto = []
with open(data_filename, 'rb') as data:
    alllines = csv.reader(data, dialect='excel')
    classes_arr = np.zeros((row_count, colm_count))  # initialize array for feeding to k-modes
    for line in alllines:
        for i in range(len(line)):
            test_class = line[i]
            if test_class != '.':
                for j in range(len(line)):
                    if i > j:  # loop over only once
                        check_class = line[j]
                        if (test_class == check_class):
                            dup_class_counter += 1
                            #print 'Found duplicate class in one record, line %d' % line_counter
                            line[j] = '.'  # unknown class
        for i in range(len(line)):
            cur_class = line[i]
            if cur_class not in classes_dict:  # add unique item to dict.
                class_counter += 1
                classes_dict[cur_class] = class_counter
                classes_arr[line_counter][i] = class_counter
            else:  # already in there
                classes_arr[line_counter][i] = classes_dict[cur_class]
        line_counter += 1
        data_sto.append(line)
####################
print 'I found %d records with a duplicate class, setting to . class' % dup_class_counter
# Now it is clean, write to new file     
with open(clean_data_filename, 'wb') as data:
    alllines = csv.writer(data, dialect='excel')
    for line in data_sto:
        alllines.writerow(line)
np.savetxt("cleaned_data_nums.txt",classes_arr,fmt='%d')
with open('data_dict.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in classes_dict.items():
        writer.writerow([key, value])
inv_classes_dict = {v: k for k, v in classes_dict.iteritems()}  # inversion of dictionary, for index lookup
#print classes_dict
#print classes_arr
# Feed to k-modes, generate knee plot
num_cluster_list = range(1, max_clusters + 1)
cost = []
centroids = []
labels = []
sse = []
vrc = []
for i in num_cluster_list:
    print "On cluster %d out of %d" % (i, max_clusters)
    km = kmodes.KModes(n_clusters=i, init='Cao', n_init=25, verbose=0)
    clusters = km.fit_predict(classes_arr)
    centroids_temp = km.cluster_centroids_
    cost_temp = km.cost_
    labels_temp = km.labels_
    sse_temp = km.sse_
    vrc_temp = km.vrc_
    cost.append(cost_temp)
    centroids.append(centroids_temp)
    labels.append(labels_temp)
    sse.append(sse_temp)
    vrc.append(vrc_temp)
#
plt.plot(num_cluster_list, cost)
plt.xlabel('Number of clusters')
plt.ylabel('Cost')
plt.title('Cost analysis from Python-based k-modes clustering')
plt.savefig('cost_plot.pdf')
plt.show()
plt.close()
#
plt.plot(num_cluster_list, sse)
plt.xlabel('Number of clusters')
plt.ylabel('Sum of squared error (SSE)')
plt.title('SSE analysis from Python-based k-modes clustering')
plt.savefig('sse_plot.pdf')
plt.close()
#
plt.plot(num_cluster_list, vrc)
plt.xlabel('Number of clusters')
plt.ylabel('Normalized Calinski-Harabasz Index (VRC)')
plt.title('VRC analysis from Python-based k-modes clustering')
plt.savefig('vrc_plot.pdf')
plt.close()
#
# print centroids for k choice and export
actual_k = raw_input("Enter your k choice from the knee plot: ")
actual_k = int(actual_k)
print "Centroids for choice k=%d, exporting to centroids.txt:" % actual_k
actual_centroids = centroids[actual_k - 1]
actual_labels = labels[actual_k - 1]
# convert indices back to actual classes
centroid_classes = []
for i in range(len(actual_centroids)):
    centroid_classes.append([])
    for j in range(len(actual_centroids[i])):
        cur_index = actual_centroids[i][j]
        class_temp = inv_classes_dict[cur_index]
        centroid_classes[i].append(class_temp)
print actual_centroids
print centroid_classes
with open("centroids.txt", 'w') as data:
    for i in range(len(centroid_classes)):
        line = str(centroid_classes[i])
        data.write(line)
        data.write('\n')
with open('labels.csv', 'wb') as data:
    alllines = csv.writer(data, delimiter='\n', dialect='excel')
    alllines.writerow(actual_labels)




