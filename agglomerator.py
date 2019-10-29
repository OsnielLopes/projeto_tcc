import time

# --- string utils ---
def clean(s):
    return s.replace('{', '').replace('}', '').replace(' ', '').replace('\n', '')

# --- tensor utils ---
def distance_v(va, vb):
    sum_squared_dif = 0
    for a, b in zip(va, vb):
        sum_squared_dif += (a - b) ** 2
    return sum_squared_dif ** 1/2


def distance(groups):
    distance_matrix = []
    min_value = {'value': 0, 'pos': (None, None)}
    for index_a, group_a in enumerate(groups):
        line = []
        for index_b, group_b in enumerate(groups):
            distances = []
            for spectre_a in group_a:
                for spectre_b in group_b:
                    distances.append(distance_v(spectre_a, spectre_b))
            minor_distance = min(distances)
            if (min_value['pos'][0] is None or min_value['value'] > minor_distance) and index_a != index_b:
                min_value['value'] = minor_distance
                min_value['pos'] = (index_a, index_b)
            line.append(minor_distance)
        distance_matrix.append(line)
    return distance_matrix, min_value # unnecessary to return the distance matrix here

# --- main routine ---
if __name__ == "__main__":
    delta_ts = []
    for rule in range(256):
        start = time.time()
        f = open('data/spectra_TXT/'+str(rule)+'.txt', 'r')
        # out = open('data/spectra_out/'+str(rule)+'.txt', 'w')
        groups = []
        f_reader = f.readlines()
        for line in f_reader:
            groups.append([[float(x) for x in clean(line).split(',')]])

        # out.write(str(groups)+'\n')
        while len(groups) > 1:
            matrix, value = distance(groups)
            for spectre in groups.pop(value['pos'][1]):
                groups[value['pos'][0]].append(spectre)
            # out.write(str(groups)+'\n')
        ellapsed_time = time.time() - start
        print('ellapsed time '+str(ellapsed_time))
        delta_ts += [ellapsed_time]
        print('estimated time '+str(sum(delta_ts)/len(delta_ts)*(255-rule)))
