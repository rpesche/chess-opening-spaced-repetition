""" Lichess editor linked function

This file is used to hold all lichess editor related code.
There is useful method for interacting with it and, for example,
ask user to draw a board on it
"""

from pathlib import Path
from urllib.parse import parse_qs, urlparse
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchWindowException


def input_chess_board() -> tuple[str, str]:
    driver = webdriver.Firefox()
    driver.get("https://lichess.org/editor")
    wait = WebDriverWait(driver, 600)

    while True:
        try:
            url = driver.current_url

            wait.until(
                lambda driver: driver.current_url != url
            )
        except (NoSuchWindowException, Exception):
            break

    o = urlparse(url)
    fen = str(Path(o.path).relative_to("/editor")).replace("_", " ")
    query = parse_qs(o.query)
    color = query["color"][0]

    return fen, color
