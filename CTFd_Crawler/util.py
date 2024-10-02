import os
import re
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List

import requests
from tqdm import tqdm

from .dataclass import ApiResult, Challenge, Important


class DownloadCrawler:
    def __init__(self, important: Important, work_directory: str):
        self.important = important
        output = work_directory
        if not os.path.exists(output):
            os.makedirs(output)
            self.output = output
        else:
            tmp_count = 1
            while True:
                if os.path.exists(f"{output}_{tmp_count}"):
                    tmp_count += 1
                else:
                    os.makedirs(f"{output}_{tmp_count}")
                    self.output = f"{output}_{tmp_count}"
                    break

    def get_output(self):
        return self.output

    def sanitize_filename(filename: str):
        sanitized_name = re.sub(r'[\/:*?"<>|]', "", filename)
        return sanitized_name

    def rearrange_download_que(self, data: List[Challenge]):
        result = []
        for i in data:
            for j in i.files:
                result.append(
                    (
                        j,
                        sanitize_filename(i.category),
                        sanitize_filename(i.name),
                        i.description,
                    )
                )
        return result

    def get_file_from_url(self, url: str):
        name = re.search(r"/files/[a-z0-9]+/([^?]+)", url).group(1)
        return name

    def add_desc(self, folder_path: str, desc: str):
        path = os.path.join(folder_path, "description.txt")
        if not os.path.isfile(path):
            with open(path, "w") as f:
                f.write(desc)
        else:
            pass

    def download_file(self, url: str, category: str, local_filename: str, desc: str):
        file_path = os.path.join(self.output, category, local_filename) + "/"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        self.add_desc(file_path, desc)
        file_path = os.path.join(file_path, self.get_file_from_url(url))

        start_time = time.time()
        response = requests.get(self.important.url + url, stream=True)
        if response.status_code != 200:
            raise Exception(
                "Status code is not 200 / please remove data filed in json file."
            )
        total_size = int(response.headers.get("content-length", 0))

        with open(file_path, "wb") as file, tqdm(
            desc=category + "/" + local_filename,
            total=total_size,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
        ) as progress_bar:
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                progress_bar.update(size)

        end_time = time.time()
        download_time = end_time - start_time
        return local_filename, download_time

    def download_all(
        self,
        data: List[Challenge],
    ):
        chals = self.rearrange_download_que(data)
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(self.download_file, chal[0], chal[1], chal[2], chal[3])
                for chal in chals
            ]
            results = []
            for future in futures:
                filename, download_time = future.result()
                results.append((filename, download_time))
        return results


class ApiManagement:
    def __init__(self, url: str, token: str):
        self.url = url.strip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Token {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def get(self, endpoint: str):
        r = self.session.get(f"{self.url}/api/v1/{endpoint.strip('/')}")
        if r.status_code != 200:
            raise Exception("Status code is not 200")
        r = ApiResult(**r.json())
        if r.success:
            return r.data
        else:
            raise Exception("Response doesn't have success key")

    def challenge(self, challenge_id: int):
        data = self.get(f"challenges/{challenge_id}")
        data = Challenge(**{i: data.get(i) for i in Challenge.__dataclass_fields__})
        return data

    def challenges(self):
        challenges = self.get("challenges")
        ids = [i["id"] for i in challenges]
        result = []
        try:
            for i in ids:
                result.append(self.challenge(i))
        except Exception as e:
            return e
        finally:
            return result
