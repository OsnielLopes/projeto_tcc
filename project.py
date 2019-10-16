from functools import reduce

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
    return distance_matrix, min_value

# --- main code ---
rule = '1'
f = open('espectros_TXT/'+rule+'.txt', 'r')
out = open('espectros_out/'+rule+'.txt', 'w')
groups = []
f_reader = f.readlines()
for line in f_reader:
    groups.append([[float(x) for x in clean(line).split(',')]])

era = 0
out.write('-----'+str(era)+'-----\n')
out.write(str(groups)+'\n')
while len(groups) > 1:
    era += 1
    matrix, value = distance(groups)
    for spectre in groups.pop(value['pos'][1]):
        groups[value['pos'][0]].append(spectre)
    out.write('-----'+str(era)+'-----\n')
    out.write(str(groups)+str(value)+'\n')
