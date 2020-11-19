import os
import time
from dotenv import load_dotenv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
load_dotenv()


class Crawler:
    TIMELINE_URL = os.environ["URL"]
    STOCK_URL = TIMELINE_URL + "?s=in-stock"
    UPCOMING_URL = TIMELINE_URL + "?s=upcoming"
    DATABASE_DIRPATH = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "database")
    CHROMEDRIVER_PATH = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "chromedriver")
    TIMEOUT = 10
    NUM_SCROLL = 20

    @classmethod
    def run(cls, mode="timeline", is_migrate=False):
        df = cls.__get_database(mode)

        if mode == "stock":
            time.sleep(30)

        driver = cls.__init_webdriver()
        wait = WebDriverWait(driver, cls.TIMEOUT)

        try:
            init_url = cls.UPCOMING_URL
            driver.get(init_url)
            time.sleep(1)

            nav_items = driver.find_elements_by_class_name("nav-items")
            for nav_item in nav_items:
                if nav_item.text == cls.__select_target_tab(mode):
                    nav_item.click()
                    time.sleep(1)
                    break

            if is_migrate:
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                buttons = driver.find_elements_by_tag_name("button")
                for button in buttons:
                    if button.text == "もっと見る":
                        button.click()
                        wait.until(EC.presence_of_all_elements_located)
                        break
                for _ in range(cls.NUM_SCROLL):
                    driver.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)
                    wait.until(EC.presence_of_all_elements_located)

            card_links = driver.find_elements_by_class_name("card-link")
            card_dicts = []
            for card_link in card_links:
                card_dicts.append({
                    "name": card_link.get_attribute("aria-label"),
                    "url": card_link.get_attribute("href")
                })
            print("{} cards were detected.".format(len(card_dicts)))

            driver.quit()

            news_list = []
            for card_dict in card_dicts:
                if not card_dict.get("url") in df["url"].values.tolist():
                    news = card_dict
                    news["is_snkrs_pass"] = "pass" in card_dict["url"] and mode == "timeline"
                    news_list.append(news)
                    df = df.append(news, ignore_index=True)
                    print("New Post: {}".format(news))
            df.to_csv(cls.__select_database_path(mode), index=False)

            return news_list

        except TimeoutException as e:
            print("TIMEOUT")
            driver.quit()
            return []

    @classmethod
    def __select_database_path(cls, mode):
        csvname = "{}.csv".format(mode)
        return os.path.join(cls.DATABASE_DIRPATH, csvname)

    @classmethod
    def __get_database(cls, mode):
        df = pd.read_csv(cls.__select_database_path(mode))
        return df

    @classmethod
    def __init_webdriver(cls):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')

        driver = webdriver.Chrome(
            executable_path=cls.CHROMEDRIVER_PATH,
            desired_capabilities=options.to_capabilities(),
            options=options
        )
        return driver

    @staticmethod
    def __select_target_tab(mode):
        if mode == "timeline":
            return "タイムライン"
        elif mode == "stock":
            return "在庫あり"
        else:
            return "タイムライン"

    @classmethod
    def __select_target_url(cls, mode):
        if mode == "timeline":
            return cls.TIMELINE_URL
        elif mode == "stock":
            return cls.STOCK_URL
        else:
            return cls.TIMELINE_URL
