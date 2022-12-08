class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.size = 0
        self.parent = parent
        self.children = {}
    
    def add_file(self, size):
        self.size += size
    
    def add_directory(self, dir_name):
        if dir_name in self.children:
            return
        self.children[dir_name] = Directory(dir_name, parent=self)

    def update_size(self):
        for child in self.children.values():
            self.size += child.update_size()
        return self.size

    def sum_at_most(self, limit):
        s = 0
        if self.size <= limit:
            s += self.size
        for child in self.children.values():
            s += child.sum_at_most(limit)
        return s
    
    def smallest_dir(self, limit):
        s = self.size if self.size >= limit else float("inf")
        for child in self.children.values():
            c_s = child.smallest_dir(limit)
            if c_s >= limit:
                s = min(s, c_s)
        return s 
            

def change_dir(name):
    global current, root
    if name == "/":
        current = root
    elif name == "..":
        current = current.parent
    else:
        if name in current.children:
            current = current.children[name]

root = Directory("/")
current = root
read_data_mode = False
with open("input.txt", "r") as f:
    for line in f:
        if line.startswith("$ cd"):
            read_data_mode = False
            change_dir(line.split(" ")[2].strip("\n"))
        elif line.startswith("$ ls"):
            read_data_mode = True
        elif read_data_mode:
            if line.startswith("dir"):
                current.add_directory(line.split(" ")[1].strip("\n"))
            else:
                current.add_file(int(line.split(" ")[0]))
# Part 1
root_size = root.update_size()
print("Part 1:", root.sum_at_most(100000))

# Part 2
avaliable_space = 70000000 - root_size
required_space = max(0, 30000000 - avaliable_space)
min_space_to_delete = root.smallest_dir(required_space)
print("Part 2:", min_space_to_delete)