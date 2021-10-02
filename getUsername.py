uName = ''

while len(uName) == 0:
    uName = input("Enter your name: ")
    if len(uName) < 0:
        break

print("Hello " +  uName)
print(len(uName))