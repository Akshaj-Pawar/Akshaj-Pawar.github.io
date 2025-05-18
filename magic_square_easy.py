def is_it_magic(square):
    #test 1: contains numbers 1 - 9
    square_contents = []
    for row in square:
        for i in row:
            if i > 9:
                return False
            if i < 1:
                return False
            if i in square_contents:
                return False
            else:
                square_contents.append(i)
    print('nothing in this square is over 9')
    #test 2i: find sum
    true_sum = 0
    for i in square[0]:
        true_sum += i
    print('sum =' + str(true_sum))
    #test 2ii: compare to rows:
    for row in square:
        rowsum = 0
        for i in row:
            rowsum += i
        if rowsum != true_sum:
            return False
    print('rows match')
    #2iii: compare to columns
    col1 = [square[0][0], square[1][0], square[2][0]]
    col2 = [square[0][1], square[1][1], square[2][1]]
    col3 = [square[0][2], square[1][2], square[2][2]]
    cols = [col1, col2, col3]
    print('columns: ' + str(cols))
    for col in cols:
        colsum = 0
        for i in col:
            colsum += i
        if colsum != true_sum:
            return False
    print('columns match')
    #2iv: compare to diagonals
    dia1 = [square[0][0], square[1][1], square[2][2]]
    dia2 = [square[0][2], square[1][1], square[2][0]]
    dias = [dia1, dia2]
    print('diagonals: ' + str(dias))
    for d in dias:
        diasum = 0
        for i in d:
            diasum += i
        if diasum != true_sum:
            return False
    print('diagonals match')
    #all tests passed
    return True

grid = [[4,3,8,4],[9,5,1,9],[2,7,6,2]]
squares = []
for i in range(len(grid) - 2):
    row = grid[i]
    for j in range(len(row) - 2):
        square_corner = row[j]
        square = [[grid[i][j], grid[i][j+1], grid[i][j+2]], [grid[i+1][j], grid[i+1][j+1], grid[i+1][j+2]], [grid[i+2][j], grid[i+2][j+1], grid[i+2][j+2]]]
        print('square: ' + str(square))
        if is_it_magic(square) == True:
            squares.append(square)
print('no of magic squares: ')
print(len(squares))

#there are more efficent ways but i think this is better because its easy to read