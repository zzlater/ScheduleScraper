import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import codecs
import MailSender

# searches for CS3505, get other class link below
# "https://student.apps.utah.edu/uofu/stu/ClassSchedules/main/1234/index.html"
val = "https://student.apps.utah.edu/uofu/stu/ClassSchedules/main/1234/sections.html?subj=ENGL&catno=5650"

# path to write to file
path = "file.txt"

# time to sleep between cycles
delay = 10


# scrapes for open availability for class 3505 and writes to file
def scrapeSeats():
    options = Options()
    options.add_argument("headless")
    options.add_argument("--headless")
    driver = webdriver.Chrome()

    # class url to search
    wait = WebDriverWait(driver, 10)
    driver.get(val)
    get_url = driver.current_url
    wait.until(EC.url_to_be(val))

    if get_url == val:
        page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'lxml')

    table1 = soup.find('tbody')
    data = {'section number': [], 'seats available': []}

    # populates data
    for j in table1.find_all('tr')[0:]:
        row_data = j.find_all('td')
        row = [i for i in row_data]

        data['section number'] = data['section number'] + [row[3]]
        data['seats available'] = data['seats available'] + [row[8]]

    # removes lxml tags & 00 (indicates section #)
    data = data.__str__().replace('<td>', '')
    data = data.__str__().replace('</td>', '')
    data = data.__str__().replace('00', '')

    # write to file
    file = codecs.open(path, 'a+')

    # clear file contents
    file.seek(0)
    file.truncate()
    file.write(data + '\n')
    print(data)
    file.close()

    driver.quit()

def checkDifferences():
    preFile = open(path, 'w+')
    pre = preFile.readline()
    scrapeSeats()
    postFile = codecs.open(path)
    post = postFile.readline()
    i = 0
    while i < len(pre):
        if post[i] != pre[i]:
            print(post)
            notifyMe(post)
            raise SystemExit
        i += 1

def notifyMe(file):
    MailSender.Send()


def ScheduleScrape(delay):
    checkDifferences()
    time.sleep(delay)
    ScheduleScrape(delay)

ScheduleScrape(delay)