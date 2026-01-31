"""
Utilities for file system management.
"""

import os
from typing import Any, Dict, List, Tuple, Union


def exists_file(filename: str) -> bool:
    """
    Check whether a file exists or not.
    :param filename: (string) the filename.
    :return: True, if the file exists; False, otherwise.
    """
    dirname = os.path.dirname(filename)
    dirname = dirname if len(dirname) != 0 else os.path.curdir
    filepath = os.path.join(dirname, filename)
    return os.path.exists(filepath)


def is_empty_file(filename: str) -> bool:
    """
    Check whether a file is empty or not.
    :param filename: (string) the filename.
    :return: True, if the file exists; False, otherwise.
    """
    with open(filename, "r") as f:
        s = f.read()
    return len(s) == 0


def empty_file(filename: str) -> None:
    """
    Delete the file.
    :param filename: (string) the filename.
    :return: None
    """
    create_dir_tree(filename)
    with open(filename, "w"):
        pass


def create_dir_tree(filename: str) -> None:
    """
    Create directory trees.
    :param filename:
    :return: (void)
    """
    dirname = os.path.dirname(filename)
    dirname = dirname if len(dirname) != 0 else os.path.curdir
    os.makedirs(dirname, exist_ok=True)


def save_list_of_numbers(filename: str, numbers: List[Union[int, float]]) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w+") as resfile:
        for value in numbers:
            resfile.write(str(value) + "\n")


def append_list_of_numbers(filename: str, numbers: List[Union[int, float]]) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "a") as resfile:
        for value in numbers:
            resfile.write(str(value) + "\n")


def save_list_of_pairs(filename: str, pairs: List[Tuple[Any, Any]]) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w+") as resfile:
        for pair in pairs:
            resfile.write("{},{}\n".format(pair[0], pair[1]))


def append_list_of_pairs(filename: str, pairs: List[Tuple[Any, Any]]) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "a") as resfile:
        for pair in pairs:
            resfile.write("{},{}\n".format(pair[0], pair[1]))


def save_csv(filename: str, list_dict: Dict[str, str]) -> None:
    """
    Saves the report onto a CSV file.
    :param filename: (string) the absolute file path.
    :param list_dict: ([dict]) the list of dictionaries.
    :return: (void)
    """
    save_header_csv(filename, list_dict)
    append_csv(filename, list_dict)


def save_header_csv(filename: str, list_dict: Dict[str, str]) -> None:
    """
    Save report headers onto a CSV file.
    :param filename: (string) the absolute file path.
    :param list_dict: ([dict]) the list of dictionaries.
    :return: (void)
    """
    with open(filename, "w+") as resfile:
        resfile.write(",".join(list_dict.keys()))
        resfile.write("\n")


def append_csv(filename: str, list_dict: Dict[str, str]) -> None:
    """
    Append the report onto a CSV file.
    :param filename: (string) the absolute file path.
    :param list_dict: ([dict]) the list of dictionaries.
    :return: (void)
    """
    with open(filename, "a+") as resfile:
        resfile.write(",".join(list_dict.values()))
        resfile.write("\n")


def save_txt(
    content: Any, filename: str, append: bool = False, empty: bool = False
) -> None:
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
    pairs = [(1, 2)]
    append_list_of_pairs(filename, pairs)
    pairs = [(2, 4)]
    append_list_of_pairs(filename, pairs)
