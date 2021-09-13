"""
Utilities for file system management.
"""
import os


def exists_file(filename):
    """
    Check whether a file exists or not.
    :param filename: (string) the filename.
    :return: True, if the file exists; False, otherwise.
    """
    dirname = os.path.dirname(filename)
    dirname = dirname if len(dirname) != 0 else os.path.curdir
    filepath = os.path.join(dirname, filename)
    return os.path.exists(filepath)


def is_empty_file(filename):
    """
    Check whether a file is empty or not.
    :param filename: (string) the filename.
    :return: True, if the file exists; False, otherwise.
    """
    with open(filename, "r") as f:
        s = f.read()
    return len(s) == 0


def empty_file(filename):
    """
    Delete the file.
    :param filename: (string) the filename.
    :return: None
    """
    create_dir_tree(filename)
    with open(filename, "w"):
        pass


def create_dir_tree(filename):
    """
    Create directory trees.
    :param filename:
    :return: (void)
    """
    dirname = os.path.dirname(filename)
    dirname = dirname if len(dirname) != 0 else os.path.curdir
    os.makedirs(dirname, exist_ok=True)


def save_list_of_numbers(filename, numbers):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w+") as resfile:
        for value in numbers:
            resfile.write(str(value) + "\n")


def append_list_of_numbers(filename, numbers):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "a") as resfile:
        for value in numbers:
            resfile.write(str(value) + "\n")


def save_list_of_pairs(filename, pairs):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w+") as resfile:
        for pair in pairs:
            resfile.write("{},{}\n".format(pair[0], pair[1]))


def append_list_of_pairs(filename, pairs):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "a") as resfile:
        for pair in pairs:
            resfile.write("{},{}\n".format(pair[0], pair[1]))


def save_csv(filename, list_dict):
    """
    Saves the report onto a CSV file.
    :param filename: (string) the absolute file path.
    :param list_dict: ([dict]) the list of dictionaries.
    :return: (void)
    """
    save_header_csv(filename, list_dict)
    append_csv(filename, list_dict)


def save_header_csv(filename, list_dict):
    """
    Save report headers onto a CSV file.
    :param filename: (string) the absolute file path.
    :param list_dict: ([dict]) the list of dictionaries.
    :return: (void)
    """
    with open(filename, "w+") as resfile:
        resfile.write(",".join(list_dict.keys()))
        resfile.write("\n")


def append_csv(filename, list_dict):
    """
    Append the report onto a CSV file.
    :param filename: (string) the absolute file path.
    :param list_dict: ([dict]) the list of dictionaries.
    :return: (void)
    """
    with open(filename, "a+") as resfile:
        resfile.write(",".join(list_dict.values()))
        resfile.write("\n")


def save_txt(content, filename, append=False, empty=False):
    """
    Save the content onto a file.
    :param content: (string) the string content to save.
    :param filename: (string) the absolute file path.
    :param append: (bool) if True, append to an existing file.
    :param empty: (bool) if True, the file is emptied.
    :return: (void)
    """
    create_dir_tree(filename)

    if empty:
        empty_file(filename)

    mode = "a+" if append else "w+"

    with open(filename, mode) as f:
        f.write(str(content))


if __name__ == "__main__":
    filename = "./test.txt"

    save_list_of_pairs(filename, [])
    l = [(1, 2)]
    append_list_of_pairs(filename, l)
    l = [(2, 4)]
    append_list_of_pairs(filename, l)
