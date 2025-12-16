class BasePage:
    def __init__(self, page):
        self.page = page

    def goto(self, url):
        """Navigate to a given URL and return the response."""
        return self.page.goto(url)
