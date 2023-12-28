import os
from python2nim.repo import git_clone, repos
from os import path
import urllib.request
from bs4 import BeautifulSoup
import re

NIM_REPO = "git@github.com:nim-lang/Nim.git"

NOT_ALLOWED_IMPORT = set({"system", "threads", "channels"})

Nim = "Nim"

cur_dir = path.abspath(path.dirname(__file__))

pro_dir = path.normpath(path.join(cur_dir, "..", ".."))

# nim_dir = path.join(pro_dir, "repos", Nim)

# nim_lib = path.join(nim_dir, "lib")

data_dir = path.join(pro_dir, "dataset")

py_lib_index = "https://docs.python.org/3.6/library/index.html"
py_std_index = "py_std_index.txt"
py_std_index = path.join(data_dir, py_std_index)

nim_lib_index = "https://nim-lang.org/docs/lib.html"
nim_std_index = "nim_std_index.txt"
nim_std_index = path.join(data_dir, nim_std_index)
# def get_nim_files(input_dir):
#     files = []
#     for (dirpath, dirnames, filenames) in os.walk(input_dir):
#         for x in filenames:
#             if x.endswith(".nim"):
#                 yield os.path.join(dirpath, x)


def get_soup(url):
    local_filename, headers = urllib.request.urlretrieve(url)
    html_file = open(local_filename)
    html = html_file.read()
    html_file.close()
    soup = BeautifulSoup(html)
    return soup


def store_py_lib_index():
    soup = get_soup(py_lib_index)
    with open(py_std_index, "w") as f:
        lines = []
        for link in soup.find_all('a'):
            text = link.get_text()
            if re.search("\s[a-z]+\s*—", text):
                lines.append(re.sub("[0-9\.]{2,}\s*", "", text))
        f.write("\n".join(lines))


def store_nim_lib_index():
    soup = get_soup(nim_lib_index)
    # with open(path.join(pro_dir, "lib.html")) as f:
    #     soup = BeautifulSoup(f.read())

    with open(nim_std_index, "w") as f:
        lines = []

        for link in soup.find_all("a", class_="reference external"):
            text = link.parent.get_text()
            if re.search("^[a-z]+\s", text):
                lines.append(text)
        f.write("\n".join(lines))

    # if not path.exists(path.join(repos, Nim)):
    #     git_clone(NIM_REPO)
    # level1 = path.join(data_dir, "level1")
    # if not path.exists(level1):
    #     os.mkdir(level1)
    # for f in get_nim_files(nim_lib):
    #     pass


def main():
    # if not path.exists(py_std_index):

    store_py_lib_index()
    store_nim_lib_index()


if __name__ == "__main__":
    main()
