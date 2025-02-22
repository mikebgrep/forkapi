from typing import Tuple, List

from playwright.sync_api import sync_playwright, TimeoutError
from playwright_stealth import stealth_sync, StealthConfig
from playwright_stealth.properties import BrowserType


def apply_stealth(page) -> None:
    ## TODO:// If we use Chrome this is working solution for scrape recipes, but not for generate duckduckgo result
    # Changing user agent to Chrome as Cloudflare look for it
    # user_agent = page.evaluate("navigator.userAgent")
    # user_agent_replaced = user_agent.replace("HeadlessChrome/", "Chrome/")
    # context = browser.new_context(
    #     user_agent=user_agent_replaced
    # )
    # config = StealthConfig(
    #     navigator_user_agent=False,
    #     navigator_plugins=False,
    #     navigator_vendor=False,
    # )

    # Disable navigator configs affect cloudflare with this we are not blocked
    config = StealthConfig(
        navigator_user_agent=False,
        browser_type=BrowserType.FIREFOX
    )

    # page = context.new_page()
    stealth_sync(page, config=config)

def get_page_content_recipe(url: str) -> Tuple[str | None, str | None] | None:
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        apply_stealth(page)
        try:
            response = page.goto(url=url, timeout=7000)
        except TimeoutError as ex:
            print(ex)
            return None, None

        try:
            # Get page content to be sure is captured regarding and issue with Chrome
            content = response.text()
            # Get thumbnail for recipies without image
            meta_content_thumbnail = page.locator('meta[property="og:image"]').nth(0).get_attribute('content',
                                                                                                    timeout=3700)
            browser.close()
        except TimeoutError as ex:
            print(ex)
            browser.close()
            return content, None

        return content, meta_content_thumbnail


def get_duckduckgo_result(url) -> List[str] | None:
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        apply_stealth(page)

        try:
            page.goto(url=url)
        except TimeoutError as ex:
            print(ex)
            return None

        href_elements = page.locator('a.result__a')
        href_values = href_elements.evaluate_all('elements => elements.map(e => e.href)')
        browser.close()

        return href_values