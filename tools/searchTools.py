# rabin karp and kmp algorithms to detect duplicated phrases or plagarized content

#Rabin-Karp String Matching Algorithm
def rabin_karp(text, pattern, q=101):
    d = 256 # Number of characters in the input alphabet (256 ASCII)
    m = len(pattern)
    n = len(text)
    h = pow(d, m - 1) % q #This helps in removing the leading digit during rolling hash
    p_hash = 0
    t_hash = 0
    positions = [] # storing the indices of the pattern found
    #Step 1: Calculate initial hash of Pattern & First window of the Text
    for i in range(m):
        _hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q
    #Step 2: Slide the pattern over the text one character at a time
    for i in range(n - m + 1):
        if p_hash == t_hash:
            if text[i:i + m] == pattern:
                positions.append(i)
        if i < n - m:
            t_hash = (d * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % q
            if t_hash < 0:
                    t_hash += q
    return positions

#Example Input:
text = "Hello World! this is Computer Science"
pattern = "Computer"
#Output
print("Rabin Karp match found at:", rabin_karp(text, pattern))



#KMP Algorithm
#Step 1: Preprocessing to compute LPS Array
def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m #Initializing LPS array with Zeros
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps
# Step 2: KMP Pattern Searching
def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    lps = compute_lps(pattern)
    positions = []
    i = j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            positions.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return positions
    
#Example Input:
text = "Hello World! this is Computer Science"
pattern = "Computer"
#Output
print("KMP match found at:", kmp_search(text, pattern))

#naive string matching algorithm
def naive_seach(text, pattern):
    positions = [] #store indicies when patterns are found
    n = len(text)
    m = len(pattern)

    #loop through all possible starting positions for i 
    for i in range(n-m+1):
        match = True #flag to track if char match
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False #mismatch ofund
                break
        if match:
            positions.append(i) #stre index of match
    return positions

#example text
text = "Hello World! this is computer science"
pattern = "computer"

#provide output
print("Naive string match found at: ", naive_seach(text,pattern))
