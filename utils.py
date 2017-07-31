import re

def exception_handler(request, exception):
    print("Request failed")

def extract_flags(text):
    pat = re.compile("\ -\w+")
    matches = re.findall(pat, text)
    return matches