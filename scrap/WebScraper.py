from __future__ import print_function
import selenium
from selenium import webdriver
import time
URL = "http://edatai.us/blog/2012/11/20/placing-kpis-different-cron-schedules"

b = webdriver.Firefox()
b.get(URL)

for i in range(2, 806):

    print(i)
    text = b.page_source.encode('utf-8')
    fp = "raw_pages/page%s.txt" % (i-1)
    print("writing", fp, "to file")
    with open(fp, "w") as text_file:
        text_file.write(text)
    try:
        next = b.find_element_by_xpath("//span[contains(text(),'%s')]" % (i))
    except selenium.common.exceptions.NoSuchElementException or selenium.common.exceptions.StaleElementReferenceException:
        print("ERROR ERROR!!!")
        i = i - 1
        print("trying again")
    next.click()
    time.sleep(2)


b.close()
