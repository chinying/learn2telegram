[![Build Status](https://travis-ci.org/chinying/learn2telegram.svg?branch=master)](https://travis-ci.org/chinying/learn2telegram)
    
This isn't really a readme, it's just information for myself  

- this is basically a API party  
- if not for herokus free tier's limits I will throw a lot more libraries at this, but I guess that can left to a local project 
- quite a lot of this is based on duckduckgo's instant answer API, and in meantime I'm trying to figure out how to parse wikipedia's infobox without using an external library  
- currently I'm working on getting the NLP to identify different kinds of queries, will probably throw some kind of classifer in front of it
- I'm aware that long_url can be done by simply checking headers, but I don't know enough about security to know if it is a good idea to do so
- will probably play with spacy v2.0 to see if it helps with the ram usage, atm the app is pushing quite close to the limits

---

## testing
`pytest`

### running individual files
`python3 -m bot.<filename>`