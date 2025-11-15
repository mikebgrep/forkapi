from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    browser.close()
    print("Firefox OK - launched and closed successfully")
