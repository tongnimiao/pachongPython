dic=[i for i in range(10000000)]
B=list(dic)
str1='*'.join(map(str,B))
with open('totalID','w')as f:
    f.write(str1)