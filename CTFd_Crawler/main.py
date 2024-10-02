import json
import logging
import os
import shutil
from dataclasses import asdict

from .dataclass import Challenge, Important
from .util import ApiManagement, DownloadCrawler

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(asctime)s - %(message)s",
    filename="ctf_crawling.log",
)


class CTFCrawler:
    def __init__(self):
        self.api = None
        self.important = None
        self.work_directory = None

    def save(self):
        if not self.important or not self.work_directory:
            logging.error("Please load the important data and work_directory")
            raise Exception("Please load the important data and work_directory")

        file_path = os.path.join(self.work_directory, f"{self.important.name}.json")
        if os.path.exists(file_path):
            backup_file_path = f"{file_path}.bak"
            shutil.copy(file_path, backup_file_path)
            logging.info(f"Existing file backed up as {backup_file_path}")
        with open(file_path, "w") as f:
            json.dump(
                {
                    "important": {
                        "name": self.important.name,
                        "url": self.important.url,
                        "token": self.important.token,
                    },
                    "data": [asdict(i) for i in self.data],
                },
                f,
                indent=4,
            )
        logging.info(f"Save the data to {file_path}")

    def important_check(self, important: dict):
        if not important.get("name"):
            logging.error("No name key in the important")
            raise Exception("No name key in the important")
        if not important.get("url"):
            logging.error("No url key in the important")
            raise Exception("No url key in the important")
        if not important.get("token"):
            logging.error("No token key in the important")
            raise Exception("No token key in the important")
        self.important: Important = Important(**important)
        return True

    def load(self, json_file_path: str):
        """
        Load the data from the file.
        """
        if not os.path.exists(json_file_path):
            raise FileNotFoundError(f"No such file: {json_file_path}")
        self.work_directory = os.path.dirname(json_file_path)
        if not self.work_directory:
            self.work_directory = "./"
        with open(f"{json_file_path}", "r") as f:
            data = json.load(f)
            if data.get("important") and self.important_check(data["important"]):
                logging.info(f"Load the data from {json_file_path}")
                self.data = []
                self.important.url = self.important.url.strip("/")
                self.api = ApiManagement(
                    self.important.url,
                    self.important.token,
                )
            else:
                raise Exception("No important key in the file. Please check the file")

    def self_load(self, name: str, url: str, token: str, work_directory: str):
        """
        Load the data from the user input.
        It save the data to file.
        """
        self.work_directory = work_directory
        if not os.path.exists(work_directory):
            os.makedirs(work_directory)
        if os.path.exists(f"{self.work_directory}/{name}.json"):
            logging.info(
                f"{self.work_directory}/{name}.json is already exists\nPlease use load method"
            )
            raise Exception(
                f"{self.work_directory}/{name}.json is already exists\nPlease use load method"
            )
        else:
            url = url.strip("/")
            self.api = ApiManagement(url, token)
            self.important = Important(name=name, url=url, token=token)
            self.data = []

    def get_challenges(self):
        if not self.api:
            logging.error("Please load the data")
            raise Exception("Please load the data")
        result = self.api.challenges()
        if type(result) == Exception:
            logging.error(result)
            raise result
        self.data = result
        self.save()
        return result

    def download_challenges(self):
        if not self.important or not self.work_directory:
            logging.error("Please set the important data and work_directory")
            raise Exception("Please set the important data and work_directory")

        self.download_crawler = DownloadCrawler(
            self.important, self.work_directory + "/archive"
        )
        logging.info("Set download crawler")
        result = self.download_crawler.download_all(self.data)
        logging.info("Download the challenges")
        for i in result:
            logging.info(f"{i} downloaded")
        self.save()
