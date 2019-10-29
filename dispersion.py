from db_index import rules_to_be_considered, dispersion

for rule in rules_to_be_considered:
    f = open('data/spectra_db_index_out/'+str(rule)+'.txt', 'r')
    f_reader = f.readlines()
    out = open('data/spectra_dispersion_out/'+str(rule)+'.txt', 'w')

    for line in f_reader:
        cluster = eval(line)
        group = cluster['group']
        group = group[0] + group[1]
        centroid = [sum([espectra[i] for espectra in group])/len(group) for i in range(len(group[0]))]
        out.write(str(dispersion(group, centroid)))

