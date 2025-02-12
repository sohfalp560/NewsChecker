from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

def scrap_news_website(web_url, story_class, link_class, title_class, body_class):
    # Configure Chrome options for headless mode (optional)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run browser in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Specify the path to your WebDriver (adjust as needed)
    service = Service('/media/soh/SohE/todo/resume/other files/tasks/i/chromedriver-linux64/chromedriver')  # Replace with your WebDriver path

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print(f"{web_url} has been started!")
        driver.get(web_url)
        print(f"{web_url} has been reached!")

        # Wait for the page to load (adjust the sleep time if necessary)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, story_class))
        )

        data = []
        print(driver)
        articles = driver.find_elements(By.CSS_SELECTOR, story_class)
        print(articles)
        if not articles:
            print("No articles found. Check the class name or website structure.")
            return data

        # Process the scraped data
        for article in articles:
            story = {}

            title_elements = article.find_elements(By.CSS_SELECTOR, title_class)
            if title_elements:
                story["title"] = title_elements[0].text.strip()

            link_elements = article.find_elements(By.CSS_SELECTOR, link_class)
            if link_elements:
                story["link"] = link_elements[0].get_attribute("href")

            body_elements = article.find_elements(By.CSS_SELECTOR, body_class)
            if body_elements:
                story["body"] = body_elements[0].text.strip()

            data.append(story)

        print(data)
        return data
    
    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        print(f"Error during scraping: {e}")
        return []

    finally:
        # Close the browser
        driver.quit()