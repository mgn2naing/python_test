uname = None

while not uname:
    uName = input("Enter your name: ")
    if len(uname) < 0:
        break

print("Hello " +  uname)
print(len(uname))
