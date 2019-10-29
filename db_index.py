from agglomerator import distance_v
import time

def dispersion(group, centroid):
    sum_squared_dif = sum([distance_v(vector, centroid) ** 2 for vector in group])
    return (sum_squared_dif / len(group)) ** 1/2
    
def similaritie(group_a, group_b):
    centroid_a = [sum([v[i] for v in group_a])/len(group_a) for i in range(len(group_a[0]))]
    centroid_b = [sum([v[i] for v in group_b])/len(group_b) for i in range(len(group_b[0]))]
    distance = distance_v(centroid_a, centroid_b)
    if distance == 0:
        return 0
    return (dispersion(group_a, centroid_a) + dispersion(group_b, centroid_b)) / distance

def db_index(cluster):
    worst_cluster_similarities = []
    for index_a, group_a in enumerate(cluster):
        similarities = []
        for index_b, group_b in enumerate(cluster):
            if index_a == index_b:
                continue
            similarities.append(similaritie(group_a, group_b))
        worst_cluster_similarities.append(max(similarities))
    return sum(worst_cluster_similarities)/len(worst_cluster_similarities)

rules_to_be_considered = {1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 18, 19, 22, 23, 24, 25, 26, 27, 28, 29, 30, 
                            33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 50, 51, 54, 56, 57, 58, 60, 62, 72, 73, 74, 
                            76, 77, 78, 90, 94, 104, 105, 106, 108, 110, 122, 126, 130, 132, 134, 138, 140, 142, 146,
                            150, 152, 154, 156, 162, 164, 170, 172, 178, 184, 200, 204, 232}

# --- main routine ---
if __name__ == "__main__":
    delta_ts = []
    for rule in rules_to_be_considered:
        start = time.time()

        f = open('data/spectra_out/'+str(rule)+'.txt', 'r')
        clusters = []
        f_reader = f.readlines()
        for line in f_reader:
            clusters.append(eval(line.replace('\n', '')))

        min_db_index = (None, 0) # (position, index_value)
        for index, cluster in enumerate(clusters):
            if not (1 < len(cluster) <= 10):
                continue
            cluster_db_index = db_index(cluster)
            if cluster_db_index < min_db_index[1] or not min_db_index[0]:
                min_db_index = (index, cluster_db_index)
        
        out = open('data/spectra_db_index_out/'+str(rule)+'.txt', 'w')
        out.write(str({'db_index': min_db_index[1],
                        'size': len(clusters[min_db_index[0]]), 
                        'group': clusters[min_db_index[0]]})
                )

        ellapsed_time = time.time() - start
        print('ellapsed in rule time '+str(ellapsed_time))
        delta_ts += [ellapsed_time]
        print('estimated time left '+str(sum(delta_ts)/len(delta_ts)*(255-rule)))