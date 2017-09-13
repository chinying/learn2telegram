import re

def exception_handler(request, exception):
    print("Request failed")

def extract_flags(text):
    pat = re.compile("\ -\w+")
    matches = re.findall(pat, text)
    return matches

# Knuth-Morris-Pratt string matching
# David Eppstein, UC Irvine, 1 Mar 2002
 
# from http://code.activestate.com/recipes/117214/
def KnuthMorrisPratt(text, pattern):
 
    '''Yields all starting positions of copies of the pattern in the text.
Calling conventions are similar to string.find, but its arguments can be
lists or iterators, not just strings, it returns all matches, not just
the first one, and it does not need the whole text in memory at once.
Whenever it yields, it will have read the text exactly up to and including
the match that caused the yield.'''
 
    # allow indexing into pattern and protect against change during yield
    T = [0] + list(text)
    P = [0] + list(pattern)
 
    m = len(P) - 1
    pi = [0] * (m+1)
    k = 0
    for q in range(2, m+1):
        while k > 0 and P[k+1] != P[q]:
            k = pi[k]
        if P[k+1] == P[q]:
            k = k + 1
        pi[q] = k
 
    # print (pi[1:], P[1:])
 
    q = 0
    for i in range(1, len(T)):
        while q > 0 and P[q+1] != T[i]:
            # print ("MISMATCH", q+1, i, pi[q])
            q = pi[q]
        if P[q+1] == T[i]:
            # print (q+1, i)
            q = q+1
        if q == m:
            print ("MATCH", (i-m))
            q = pi[q]
 