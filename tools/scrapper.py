from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import polars as pl
import requests
from requests.cookies import create_cookie
import os
from dotenv import load_dotenv

load_dotenv()

options = Options()
prefs = {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "profile.default_content_setting_values.notifications": 2,
}
options.add_experimental_option("prefs", prefs)
options.add_argument("--incognito")


driver = webdriver.Chrome(options=options)


def identification():
    driver.get("https://pro.beligne.fr/")
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "tiers_email"))
    )
    email_input.send_keys(os.getenv("EMAIL"))
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "tiers_motdepasse"))
    )
    password_input.send_keys(os.getenv("PASSWORD"))
    password_input.send_keys(Keys.RETURN)


def search_product(ref):
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search_keywords"))
    )
    search_input.clear()
    search_input.send_keys(ref)
    search_input.send_keys(Keys.RETURN)


def download_image(driver, img_url):
    os.makedirs("downloaded_images", exist_ok=True)
    if (
        str.replace(os.path.basename(img_url), ".jpg", "")[-2] != "_"
        and str.replace(os.path.basename(img_url), ".jpg", "")[-3] != "_"
    ):
        os.makedirs(
            f"downloaded_images/{str.replace(os.path.basename(img_url),".jpg", "")}",
            exist_ok=True,
        )

    session = requests.Session()
    for cookie in driver.get_cookies():
        new_cookie = create_cookie(
            name=cookie["name"],
            value=cookie["value"],
            domain=cookie.get("domain"),
            path=cookie.get("path", "/"),
            secure=cookie.get("secure", False),
            rest={"HttpOnly": cookie.get("httpOnly", False)},
            expires=cookie.get("expiry"),
        )
        session.cookies.set_cookie(new_cookie)
    filename = ""
    if (
        str.replace(os.path.basename(img_url), ".jpg", "")[-2] != "_"
        and str.replace(os.path.basename(img_url), ".jpg", "")[-3] != "_"
    ):
        print(str.replace(os.path.basename(img_url), ".jpg", "")[-2])
        filename += (
            str.replace(os.path.basename(img_url), ".jpg", "")
            + "/"
            + os.path.basename(img_url)
        )

    else:
        dir = str.replace(os.path.basename(img_url), ".jpg", "").split("_")
        for i in range(0, len(dir) - 1):
            filename += dir[i] + "_"
        filename = filename[:-1]
        filename += "/"
        filename += os.path.basename(img_url)

    filepath = os.path.join("downloaded_images", filename)

    response = session.get(img_url)
    if response.status_code == 200:
        with open(filepath, "wb") as f:
            f.write(response.content)
            print(f"Image downloaded: {filepath}")


def get_ref(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "fiche-article-reference"))
    )
    ref = driver.find_element(By.CLASS_NAME, "fiche-article-reference").text.split(":")
    return ref[-1]


def get_title(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "article-list-libelle"))
    )
    title = driver.find_element(By.CLASS_NAME, "article-list-libelle")
    return title


def get_article_data():
    data = {}
    data["ref"] = get_ref(driver)
    data["title"] = get_title(driver)

    left_panel = driver.find_element(
        By.CSS_SELECTOR, 'td[align="left"][valign="top"][width="324"]'
    )

    links = left_panel.find_elements(By.TAG_NAME, "a")

    for link in links:
        if link.get_attribute("href").find(".jpg") != -1:
            download_image(driver, link.get_attribute("href"))

    return data


def go_to_product_page():
    product_cell = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tdCelluleItem1"))
    )
    WebDriverWait(product_cell, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "a"))
    )
    if (
        product_cell.find_element(By.TAG_NAME, "a")
        .get_attribute("title")
        .find("PRESENTOIR")
        == -1
        and product_cell.find_element(By.TAG_NAME, "a")
        .get_attribute("title")
        .find("VITRINE")
        == -1
    ):
        driver.get(product_cell.find_element(By.TAG_NAME, "a").get_attribute("href"))
        return True

    else:
        return False


def get_data(refList):
    identification()
    for ref in refList:
        search_product(ref)
        productPage = go_to_product_page()
        if productPage:
            get_article_data()
