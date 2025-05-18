
def merge(unmerged):
    print('unmerged: ' + str(unmerged))
    if len(unmerged) == 1:
        return unmerged
    else:
        merged = []
        s = []
        while len(unmerged) > 1:
            print('unmerged' + str(unmerged))
            l1 = unmerged[0]
            print(l1)
            l2 = unmerged[1]
            print(l2)
            if len(l1) == 0:
                for i in l2:
                    s.append(i)
                unmerged.pop(1)
                unmerged.pop(0)
                print('s =' + str(s))
                merged.append(s.copy())
                s = []
            elif len(l2) == 0:
                for i in l1:
                    s.append(i)
                unmerged.pop(1)
                unmerged.pop(0)
                print('s =' + str(s))
                merged.append(s.copy())
                s = []
            else:
                if l1[0] > l2[0]:
                    s.append(l2[0])
                    l2.pop(0)
                else:
                    s.append(l1[0])
                    l1.pop(0)
        if len(unmerged) == 1:
            merged.append(unmerged[0])
        return merge(merged)

def select(list):
    for i in range(len(list)):
        min = list[i]
        min_pos = i
        for j in range(i, len(list)):
            if list[j] < min:
                min = list[j]
                min_pos = j
        list[min_pos] = list[i]
        list[i] = min
    return(list)

def insert(list):
    for i in range(1, len(list)):
        x = list[i]
        for j in range(0, i):
            if list[j] > x:
                list.pop(i)
                list.insert(j, x)
                break
    return(list)

def bubble(list):
    for i in range(len(list) - 1):
        for j in range(len(list)-1):
            if list[j] > list[j+1]:
                x = list[j]
                list[j] = list[j+1]
                list[j+1] = x
    return(list)

#first split an array into bits 1 index long
#list = [1, 5, 3, 8, 7, 4, 2, 6]
#print(select(list))
#list = [1, 5, 3, 8, 7, 4, 2, 6]
#print(insert(list))
#list = [1, 5, 3, 8, 7, 4, 2, 6]
#print(bubble(list))
list = [1, 5, 3, 8, 7, 4, 2, 6, 10, 11, 9]
print(list)
segs = []
for i in list:
    seg = []
    seg.append(i)
    segs.append(seg)
print(merge(segs))