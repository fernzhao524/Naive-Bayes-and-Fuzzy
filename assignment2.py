import scipy.stats

my_naive_bayes_list = [[[41, 6], [37, 4], [10, 2]],
                       [[53, 9], [27, 3], [12, 2]],
                       [[66, 10], [55, 6], [22, 6]],
                       [[61, 9], [52, 7], [26, 8]]]

listAllP = [0.30, 0.21, 0.14, 0.35]
breedName = ['beagle', 'corgi', 'husky', 'poodle']


myFuzzyList = [[[0, 0, 40, 50], [40, 50, 60, 70], [60, 70, 100, 100]],
               [[0, 0, 25, 40], [25, 40, 50, 60], [50, 60, 100, 100]],
               [[0, 0, 5, 15], [5, 15, 20, 40], [20, 40, 100, 100]]]

def findCondProb(inputNumber):
    list1 = []

    for i in range(len(my_naive_bayes_list)):

        row = []
        for j in range(len(my_naive_bayes_list[i])):
            row.append(scipy.stats.norm(my_naive_bayes_list[i][j][0], my_naive_bayes_list[i][j][1]).pdf(inputNumber[j]))
        list1.append(row)

    return list1


def naive_bayes_classifier(input_list):
    listL = findCondProb(input_list)
    probEq = []
    for i in range(len(listL)):
        product = 1
        for j in range(len(listL[i])):
            product *= listL[i][j]
        probEq.append(product * listAllP[i])

    evidence = 0
    for i in range(len(probEq)):
        evidence += probEq[i]

    class_probabilities = [x / evidence for x in probEq]

    maxnumber = 0
    most_likely_class = ''
    for i in range(len(class_probabilities)):
        if (class_probabilities[i] > maxnumber):
            maxnumber = class_probabilities[i]
            most_likely_class = breedName[i]

    return most_likely_class, class_probabilities


def findFuzzyM(input_list):
    list = []
    for i in range(len(myFuzzyList)):
        row = []
        for j in range(len(myFuzzyList[i])):
            if (input_list[i] <= myFuzzyList[i][j][0]):
                row.append(0)
            elif (input_list[i] > myFuzzyList[i][j][0] and input_list[i] < myFuzzyList[i][j][1]):
                row.append((input_list[i] - myFuzzyList[i][j][0]) / (myFuzzyList[i][j][1] - myFuzzyList[i][j][0]))
            elif (input_list[i] >= myFuzzyList[i][j][1] and input_list[i] <= myFuzzyList[i][j][2]):
                row.append(1)
            elif (input_list[i] > myFuzzyList[i][j][2] and input_list[i] < myFuzzyList[i][j][3]):
                row.append((myFuzzyList[i][j][3] - input_list[i]) / (myFuzzyList[i][j][3] - myFuzzyList[i][j][2]))
            else:
                row.append(0)
        list.append(row)

    return list

#testing Question5 Godel
'''
def helperT(x,y):
    return min(x,y)
def helperS(x, y):
    return max(x,y)
'''
#Goguen
def helperT(x, y):
    return x * y


def helperS(x, y):
    return (x + y) - (x * y)


def fuzzy_classifier(input_list):
    fuzzyProbM = findFuzzyM(input_list)
    class_memberships = []
    # rule1
    class_memberships.append(helperT(fuzzyProbM[1][1], helperS(fuzzyProbM[0][0], fuzzyProbM[2][0])))
    # rule2
    class_memberships.append(helperT(fuzzyProbM[0][1], helperT(fuzzyProbM[1][0], fuzzyProbM[2][1])))
    # rule3
    class_memberships.append(helperT(fuzzyProbM[0][2], helperT(fuzzyProbM[1][2], fuzzyProbM[2][1])))
    # rule4
    class_memberships.append(helperT(helperS(fuzzyProbM[0][1], fuzzyProbM[1][1]), fuzzyProbM[2][2]))

    maxnumber = 0
    highest_membership_class = ''
    for i in range(len(class_memberships)):
        if (class_memberships[i] > maxnumber):
            maxnumber = class_memberships[i]
            highest_membership_class = breedName[i]
    if not highest_membership_class:
        print("\nNot able to find the class using Fuzzy_classifier!")

    return highest_membership_class, class_memberships


if __name__ == '__main__':
    inputNumber = []
    ''' 
If you don't like enter value 3 time（our test case）
add girth, height, weight to the empty list of inputNumber above
for example inputNumber=[59,32,17]
here is our test case, 
you can comment this part below
    '''
    girthInput = input("Please give Girth: ")
    inputNumber.append(int(girthInput))
    
    heightInput = input("Please give Height: ")
    inputNumber.append(int(heightInput))

    weightInput = input("Please give Weight: ")
    inputNumber.append(int(weightInput))


    print("My Input is ", inputNumber)

    naive_bayes_class, naive_bayes_prob = naive_bayes_classifier(inputNumber)
    print("naive_bayes_classifier:\n", '"', naive_bayes_class, '" ,', naive_bayes_prob)

    highest_membership_class, class_memberships = fuzzy_classifier(inputNumber)
    print("fuzzy_classifier:\n", '"', highest_membership_class, '" ,', class_memberships)
