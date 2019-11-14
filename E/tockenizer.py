import nltk
nltk.download('punkt')

with open('page_pl.txt', 'r') as f:
    content = f.read()

with open('page_pl_t.txt', 'a') as f2:
    content = nltk.sent_tokenize(content)
    for i in content:
        f2.write(i + "\n")

f.close()
f2.close()