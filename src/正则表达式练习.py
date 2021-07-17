import re

strs = "我的电话:1999999999,他的电话:7778889999"

res = re.findall(r'\d+', strs)
print(res)

# search返回的是match对象, 拿数据需要.group()
res1 = re.search(r'\d+', strs)
print(res1.group())

# match是从头开始匹配 ^
res2 = re.match(r'\d+', strs)
print(res2.group())

# finditer: 匹配字符串中所有的内容(返回的是一个迭代器)
it = re.finditer(r'\d+', strs)
for i in it:
    print(i.group())
