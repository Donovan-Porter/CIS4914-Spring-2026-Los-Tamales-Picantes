import io
import os
import json

'''
file = open("test.json")
vocab = json.load(file)

print(vocab["groups"][0]["title-es"])
print(vocab["groups"][0]["title-en"])
print()

for word in vocab["groups"][0]["vocabulary"] :
    print(f'{word["es"]} == {word["en"]}')



file1 = open("vocab1.json")
vocab1 = json.load(file1)


for group in vocab1["groups"] :
    print(f'{group["title-es"]} == {group["title-en"]}')
    print()

    for word in group["vocabulary"] :
        print(f'{word["es"]} == {word["en"]}')



file2 = open("vocab2.json")
vocab2 = json.load(file2)

for group in vocab2["groups"] :
    print(f'{group["title-es"]} == {group["title-en"]}')
    print()

    for word in group["vocabulary"] :
        print(f'{word["es"]} == {word["en"]}')
'''

for n in range(1, 7) :
    print(str(n))
    filename = "grammar" + str(n) + ".json"
    file = open(filename, encoding='utf-8')
    grammar = json.load(file)

    for group in grammar["groups"] :
        print(f'{group["title"]}')
        print()
        for example in group["examples"] :
            print(f"{example['integral']} ==> {example['derivative']}")
        print()
    print()