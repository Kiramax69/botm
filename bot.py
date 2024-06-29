from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Опционально, для запуска без графического интерфейса

try:
    driver = webdriver.Chrome(options=options)
    driver.get("http://www.google.com")
    print("Title: ", driver.title)
finally:
    driver.quit()
