with open('page.txt', 'r') as f:
    content =  f.read().replace("\\n", "").replace("\\t", "")

with open('page_pl.txt', 'w') as f2:
    f2.write(content)
f.close()
f2.close()