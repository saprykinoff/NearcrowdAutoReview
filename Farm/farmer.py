import datetime
import requests
import time
import config
import warnings
if not config.verify:
    warnings.filterwarnings("ignore")
class Farmer:
    links: dict[str, str] = dict()
    mode = "ncf"  # "cf" / "ncf"
    running = False
    __delay = 5


    __lst_rq = "??:??"
    __lst_time = 0
    __acc = ""
    def __init__(self, acc):
        self.links = dict()
        self.__acc = acc
        with open(f"links/{acc}.txt", "r") as f:
            links = f.readlines()
            for x in links:
                prv = x.strip()
                x = x.strip().split("/")
                tp = x[4]
                numb = x[5]
                self.links[f"{numb}/{tp}"] = prv
        print(f"{acc} was initiated, sz = ", len(self.links))

    def status(self):
        link = ""
        if (self.mode == "cf"):
            link = self.links['42/taskset']
        else:
            link = self.links['43/taskset']
        try:
            resp = requests.get(link, verify=config.verify)
            resp.raise_for_status()
            stat = resp.json()
            if (stat['status'] == "free"):
                return "No review " + self.__lst_rq
            if (stat['status'] == 'has_review'):
                return stat['time_left']
            if (stat['status'] == 'has_task'):
                return "Has task"
            return stat
        except requests.exceptions.HTTPError as e:
            print(datetime.datetime.now(), "request error", e)
            return "No review: request error"

    def __request(self):
        if (time.time() < self.__lst_time + self.__delay):
            # print("Too frequently")
            return False
        link = ""
        if (self.mode == "cf"):
            link = self.links['42/claim_review']
        else:
            link = self.links['43/claim_review']
        # print(f"request by {self.__acc}: {link[25:40]}, {time.time() - self.__lst_time}")

        try:
            resp = requests.get(link, verify=config.verify)
            resp.raise_for_status()
            text = resp.text
            self.__lst_time = time.time()
            return text
        except requests.exceptions.HTTPError as e:
            print(datetime.datetime.now(), "request error", e)
            return False



    def run(self):
        self.running = True
        while (self.running):
            s = self.__request()

            if (s == False):
                time.sleep(0.2)
                continue

            if (s == "no_reviews"):
                now = datetime.datetime.now()
                self.__lst_rq =  now.strftime('%M:%S')
                continue
            elif (s == "need_more_tasks"):
                self.__lst_rq = ": Need more tasks"
            else:
                stat = self.status()
                self.__lst_rq = s
                if ("No review" in stat):
                    print("Error: " + s)



