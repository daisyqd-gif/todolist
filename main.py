

# to-do list functions
class ToDo():
    def __init__(self):
        self.lst=[]
    def insert(self, name : str):
        self.lst.append(name)

    def edit(self, index : int, name : str):
        self.lst[index]=name

    def pop(self)->str:
        return self.pop(0)

    def pop(self, index : int):
        return self.lst.pop(index)

    def __str__(self):
        counter=0
        output=""
        for i in self.lst:
            output+=str(counter)
            output+=": "
            output+=i
            output+="\n"
            counter+=1
        
        return output
# main function
def __main__():
    list = []
    this=ToDo()
    while True:
        try:
            inp=input("Press 1 to add to the to do list, press 2 to pop a specific item from the list, press 3 to edit an element, press 4 to see your to do list: ")
            match inp:
                case "1":
                    inp=input("Please enter the name of the item you would like to add: ")
                    this.insert(inp)
                case "2":
                    inp=input("Please enter the index of the item you would like to pop: ")
                    print(this.pop(int(inp)))
                case "3":
                    inp=input("Please enter the index of the item you would like to edit: ")
                    inp2=input("Please enter the new name of the item you would like to edit: ")
                    this.edit(int(inp),inp2)
                case "4":
                    print(this)
                case _:
                    print("Invalid input")
                    continue
        except IndexError:
            print("Index invalid! Use another index or press 4 to see the list")
__main__()


