from CTFd_Crawler import CTFCrawler

crawler = CTFCrawler()
# crawler.self_load("test_ctf", "https://ctfd.based/site", "****************************************************************", "./test_ctf")
crawler.load("./test_ctf.json")
print("load")
print(crawler.important)
res = crawler.get_challenges()
print("get_challenges")
crawler.download_challenges()
