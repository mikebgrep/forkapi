from typing import Tuple, List

from playwright.sync_api import sync_playwright, TimeoutError
from playwright_stealth import stealth_sync, StealthConfig
from playwright_stealth.properties import BrowserType
from playwright.sync_api import sync_playwright


class Browser:

    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.firefox.launch(headless=True)
        self.page = self.browser.new_page()
        self.apply_stealth()


    def close(self):
        self.browser.close()
        self.playwright.stop()

    def apply_stealth(self) -> None:
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
        stealth_sync(self.page, config=config)

    def get_page_content_recipe(self, url: str) -> Tuple[str | None, str | None] | None:
        try:
            response = self.page.goto(url=url, timeout=7000)
            content = response.text()
        except TimeoutError as ex:
            print(ex)
            return None, None

        try:
            # Get thumbnail for recipies without image
            meta_content_thumbnail = self.page.locator('meta[property="og:image"]').nth(0).get_attribute('content', timeout=3700)
        except TimeoutError as ex:
            print(ex)
            return content, None

        return content, meta_content_thumbnail


    def get_duckduckgo_result(self, url) -> List[str] | None:
        try:
            self.page.goto(url=url)
        except TimeoutError as ex:
            print(ex)
            return None

        href_elements = self.page.locator('a.result__a')
        href_values = href_elements.evaluate_all('elements => elements.map(e => e.href)')

        return href_values