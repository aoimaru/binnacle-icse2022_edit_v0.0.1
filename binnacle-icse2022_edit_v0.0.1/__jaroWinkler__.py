# coding: utf-8
# Your code here!

def getNumRangeMatchChar(S1: str, S2: str, distance=-1):
    L1 = len(S1); L2 = len(S2)
    ignored_distance = False
    
    if distance < 0 : ignored_distance = True
    
    counter = 0
    
    for i in range(L1):
        From = i
        Under = L2
        if not ignored_distance:
            From = 0 if i<distance else i-distance
            Under = int(L2) if i+distance>=L2 else i+distance
        
        for j in range(From, Under):
            if S1[i]==S2[j]: counter+=1
    return counter

def getRangeMatchChar(S1, S2, distance=-1):
    L1 = len(S1); L2 = len(S2)
    ignored_distance = False
    
    if distance < 0 : ignored_distance = True
    
    ret = ""
    for i in range(L1):
        From = i
        Under = L2
        if not ignored_distance:
            From = 0 if i<distance else i-distance
            Under = L2 if i+distance>=L2 else i+distance
        
        for j in range(From, Under):
            if S1[i]==S2[j]: ret+=S1[i]
    
    return ret
    
def getNumTransposition(S1, S2):
    c = 0
    L1 = len(S1); L2 = len(S2)
    for i in range(min(L1, L2)):
        if S1[i] != S2[i]: c+=1
    
    return c

def getJaroDistance(S1, S2):
    L1 = len(S1); L2 = len(S2)
    distance = max(L1, L2)
    if distance<0: return -1
    distance = int(distance/2)-1
    if distance<0: return -1
    
    match = getNumRangeMatchChar(S1, S2, distance)
    trans = getNumTransposition(getRangeMatchChar(S1, S2, distance), getRangeMatchChar(S1, S2, distance))
    m = match
    t = trans/2
    
    return (m/L1+m/L2+(m-t)/match)/3
    
def getLengthOfCommonPrefix(S1, S2):
    L1 = len(S1); L2 = len(S2)
    c = 0
    for i in range(min(L1, L2)):
        if (S1[i]==S2[i]):
            c+=1
        else:
            break
    return c

def getJaroWinklerDistance(S1, S2, scaling=0.1):
    if scaling<0: return -1
    j = getJaroDistance(S1, S2)
    return j+getLengthOfCommonPrefix(S1, S2)*scaling*(1-j)



def main():
    S1 = "hello"
    S2 = "helloWorld"
    S3 = "vfdosbfpvuobsfd@:vasbdv"
    JW = getJaroWinklerDistance(S1, S2)
    print(JW)


if __name__ == "__main__":
    main()