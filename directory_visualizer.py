import os
import time

MAX_ATTEMPTS = 3


class Node:
    """ Class that represents the file directories of a folder system. Each folder is a node.
    Allows for tree structure, such that other nodes can be nested in the property Node.subnodes
    Each node has a unique id, which allows for tracking how many objects are instantiated (folders analyzed)
    Nodes only register a number of files in the immediate folder contents, i.e. folder_name (12 files)
    Each folder also has "tab_chars", which represent the line structures created by the helper function
    """

    # This variable is incremented up by one every time Node class is instantiated
    # Gives each object from this class a unique id, which allows for tracking how many are created
    id = 0

    def __init__(self, path, tab_chars):
        self.path = path
        self.name = os.path.basename(path)
        self.tab_chars = tab_chars
        self.folders = \
            [os.path.join(self.path, f) for f in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, f))]
        self.files = self.count_files(path)
        self.subnodes = []
        Node.id += 1
        self.id = Node.id

    # This is basically just a helper function that is used in __init__, so it's static and doesn't access the instance
    @staticmethod
    def count_files(path):
        files = 0
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)) and not (file.startswith("~") or file.endswith(".db")):
                files += 1
        return files

    def print_slice(self):
        return self.tab_chars + f"{self.name} ({self.files} file{'s' if self.files != 1 else ''})"


def create_file_tree(tree_directory, tab_chars=''):
    node = Node(tree_directory, tab_chars)
    if node.id % 50 == 0:
        print(f'Scanning at: {node.path} \n...')

    # Iterate through the folders
    for index, folder in enumerate(node.folders, start=1):
        connector = "   "
        if node.tab_chars.endswith("├─ "):
            connector = "│  "
        if index == len(node.folders):
            child_node = create_file_tree(folder, node.tab_chars[:-3] +
                                          f"{connector}└─ ")
            node.subnodes.append(child_node)
        else:
            child_node = create_file_tree(folder, node.tab_chars[:-3] +
                                          f"{connector}├─ ")
            node.subnodes.append(child_node)

    return node


def print_file_tree(tree):
    # for debugging
    print(tree.print_slice())
    for t in tree.subnodes:
        print_file_tree(t)
    return


def make_file_tree_text(tree):
    txt_tree = tree.print_slice() + '\n'
    for t in tree.subnodes:
        txt_tree += make_file_tree_text(t)
    return txt_tree


def get_valid_directory_path():
    print("A simple program to display the contents of a file system visually. -WW\n")
    print('Press "CTRL + C" to cancel execution\n')
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        print("Enter a valid directory path, then press enter")
        directory_path = input(r"eg., M:\IMAGES\RRMOJIS: ").strip(
            '\'" ')  # Remove leading/trailing spaces, single or double quotes
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            return directory_path
        else:
            print("Invalid directory path. Please try again.")
            attempts += 1
    print("No valid directory path provided. Ending the program.")


def create_txt_file(tree_dir):
    filename = f'(MAP) {os.path.basename(tree_dir)}.txt'
    my_tree = create_file_tree(tree_dir)
    tree_txt = make_file_tree_text(my_tree)
    output_file = os.path.expanduser(f"~/Downloads/{filename}")
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(tree_txt)
    print("Directory tree saved to:", output_file)
    time.sleep(3)


if __name__ == "__main__":
    create_txt_file(get_valid_directory_path())

