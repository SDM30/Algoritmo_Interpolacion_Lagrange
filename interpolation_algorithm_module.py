def lagrange_interpolation(nodes, y_i, x):
    approximation = 0
    l = []
    for k in range(len(nodes)):
        l_k = 1
        x_k = nodes[k]
        for i in range(len(nodes)):
            if k != i:
                l_k *= (x - nodes[i])/(x_k - nodes[i])
                
        l.append(l_k)
    
    for k in range(len(nodes)):
        approximation += l[k]*y_i[k]
        
    return round(approximation)

def interpolate_by_list(nodes, y_i, x):
    return [lagrange_interpolation(nodes, y_i, value) for value in x]
        
    