 
#Naive String matching alorithm
def naive_search(text, pattern):
    ositions = [] #to store indices where patterns are found
    n = len(text)
    m = len(pattern)
    #loop through all possible starting positions for i
    for i in range(n - m + 1):
        match = True #Flag to track if characters match
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False #Mismatch found
                break
        if match:
            positions.append(i) #Store the index of the match
    return positions
    #Example Input:
    text = "Hello World! this is Computer Science"
    pattern = "Computer"
    #Output
    print("Naive String match found at:", naive_search(text, pattern))
