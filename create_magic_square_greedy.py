import numpy as np

def find_divergence(average_sum, mun_square):
    current_sums = []
    divergence = 0
    for r in mun_square:
        rowsum = 0
        for i in r:
            rowsum += i
        current_sums.append(rowsum)
    col1 = [mun_square[0][0], mun_square[1][0], mun_square[2][0]]
    col2 = [mun_square[0][1], mun_square[1][1], mun_square[2][1]]
    col3 = [mun_square[0][2], mun_square[1][2], mun_square[2][2]]
    cols = [col1, col2, col3]
    for col in cols:
        colsum = 0
        for i in col:
            colsum += i
        current_sums.append(colsum)
    dia1 = [mun_square[0][0], mun_square[1][1], mun_square[2][2]]
    dia2 = [mun_square[0][2], mun_square[1][1], mun_square[2][0]]
    dias = [dia1, dia2]
    for d in dias:
        diasum = 0
        for i in d:
            diasum += i
        current_sums.append(diasum)
    print(current_sums)
    for sum in current_sums:
        divergence += abs(average_sum - sum)
    return(divergence)

def increment(mun_square, actions, average_sum, increments_made, min_divergence):
    mun_square = np.array(mun_square)
    min_square = mun_square
    changed = False
    for action in actions:
        A = mun_square + action
        divergence = find_divergence(average_sum, A)
        if divergence < min_divergence:
            min_square = A
            min_divergence = divergence
            changed = True
            print('changed, new min divergence: ' + str(min_divergence))
    if not changed:
        return(min_square)
    else:
        increments_made.append(min_square)
        print('new min_square: ')
        print(min_square)
        return(increment(min_square, actions, average_sum, increments_made, min_divergence))


mun_square = [[4, 2, 7], [9, 5, 7], [0, 6, 7]]
average_sum = 15
actions = [np.array([[1, 0, 0],[0, 0, 0],[0, 0, 0]]), 
           np.array([[0, 1, 0],[0, 0, 0],[0, 0, 0]]), 
           np.array([[0, 0, 1],[0, 0, 0],[0, 0, 0]]), 
           np.array([[0, 0, 0],[1, 0, 0],[0, 0, 0]]), 
           np.array([[0, 0, 0],[0, 1, 0],[0, 0, 0]]), 
           np.array([[0, 0, 0],[0, 0, 1],[0, 0, 0]]), 
           np.array([[0, 0, 0],[0, 0, 0],[1, 0, 0]]), 
           np.array([[0, 0, 0],[0, 0, 0],[0, 1, 0]]), 
           np.array([[0, 0, 0],[0, 0, 0],[0, 0, 1]]), 
           np.array([[-1, 0, 0],[0, 0, 0],[0, 0, 0]]), 
           np.array([[0, -1, 0],[0, 0, 0],[0, 0, 0]]), 
           np.array([[0, 0, -1],[0, 0, 0],[0, 0, 0]]), 
           np.array([[0, 0, 0],[-1, 0, 0],[0, 0, 0]]), 
           np.array([[0, 0, 0],[0, -1, 0],[0, 0, 0]]), 
           np.array([[0, 0, 0],[0, 0, -1],[0, 0, 0]]), 
           np.array([[0, 0, 0],[0, 0, 0],[-1, 0, 0]]), 
           np.array([[0, 0, 0],[0, 0, 0],[0, -1, 0]]), 
           np.array([[0, 0, 0],[0, 0, 0],[0, 0, -1]])]

print(find_divergence(15, mun_square))
mag_square = increment(mun_square, actions, average_sum, [], 10000)
print(mag_square)
#print(increments)