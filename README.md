# CTFd-Crawler

## Overview

CTFd-Crawler is a tool designed to efficiently manage and download CTF challenge files.
It organizes downloads into categories, supports multi-threaded downloads for speed enhancement, logs all activities, and stores metadata in JSON format.

## Features

1. Downloads
   1. Organize downloaded files into subdirectories based on challenge categories.
   2. Implement multi-threading to download multiple files simultaneously, improving overall download speed.
   3. Create a detailed log of the download process, including any errors and warnings.
   4. Show detailed progress of downloading.
2. It save description into description.txt in each challenge directory.
3. Directory rules.
4. If contents are in a directory, it create another directory (add numbering).
5. If contents are not in a directory, the files just saved in it.
6. All file / folder name including space is replaced with underscore.
7. There are two options in loading information about CTF.
8. Load from file (have to set directory when use crawler. if not, It basically set to current directory)
9. Load from user input (not recommended, automatically saved into file)
10. All information about ctf (name, token, url, download location) saved into file with json format for convenient access.
11. Crawling all challenges and dump them into file too.

## File Structure

### Load

#### Before

```plaintext
.
└── ctf.json # contains basic information about CTF (refer to the sample folder)
```

### After

```plaintext
.
├── ctf.json # add challenges information
└── challenges
    ├── pwn
    │   ├── challenge1
    │   │   ├── description.txt
    │   │   ├── file1
    │   │   └── file2
    │   └── challenge2
    │       ├── description.txt
    │       ├── file1
    │       └── file2
    └── rev
        ├── challenge1
        │   ├── description.txt
        │   ├── file1
        │   └── file2
        └── challenge2
            ├── description.txt
            ├── file1
            └── file2
```

### Self Load

#### Before

```plaintext
.
```

#### After

```plaintext
.
├── ctf.json
└── archive
    ├── pwn
    │   ├── challenge1
    │   │   ├── description.txt
    │   │   ├── file1
    │   └── challenge2
    │       ├── description.txt
    │       ├── file1
    └── rev
        ├── challenge1
        │   ├── description.txt
        │   ├── file1
        └── challenge2
            ├── description.txt
            ├── file1
```

## Usage

```python
from CTFd_Crawler import CTFCrawler

crawler = CTFCrawler()
# crawler.self_load("test_ctf", "https://ctfd.based/site", "****************************************************************", "./test_ctf")
crawler.load("./test_ctf.json")
print("load")
print(crawler.important)
res = crawler.get_challenges()
print("get_challenges")
crawler.download_challenges()
```

you can choose one option between `load` and `self_load`. `load` is loading from file and `self_load` is loading from user input.
