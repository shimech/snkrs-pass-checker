import os
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import warnings
warnings.simplefilter("ignore")


class Client:
    DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "database/url.csv")

    @classmethod
    def request(cls):
        df = pd.read_csv(cls.DATABASE_PATH)
        df_search = df.query("not is_access")

        snkrs_pass_urls = []
        for i in df_search["id"].values.tolist():
            record = df_search.query("id == {}".format(i))
            url = record["url"].values[0]
            response = requests.get(url)
            time.sleep(1.5)
            print("{} {}".format(url, response))
            if response.status_code == 200:
                is_new_snkrs_pass = True

                bs = BeautifulSoup(response.text, "html.parser")
                h1s = bs.find_all("h1")
                if len(h1s) == 0:
                    is_new_snkrs_pass = False
                for h1 in h1s:
                    if h1.text == "404エラー":
                        is_new_snkrs_pass = False
                        break

                if is_new_snkrs_pass:
                    print("New SNKRS PASS: {}".format(url))
                    snkrs_pass_urls.append(url)
                    df["is_access"][df["id"] == i] = True

        df.to_csv(cls.DATABASE_PATH, index=False)

        return snkrs_pass_urls
