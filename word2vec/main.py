from preprocess_copy import clean
from wiki_dump_reader import Cleaner, iterate
import time 
cleaner = Cleaner()


w = open("cleanWikiText_.txt","w",encoding="utf8")


start = time.time()
for title, text in iterate('tr-wikipedia.xml'):
    text = cleaner.clean_text(text)

    text, links = cleaner.build_links(text)

    cleaned_text = clean(text)
    
    
    try:
        w.writelines(text+"\n")
    except: pass
print(time.time()- start)  

w.close()