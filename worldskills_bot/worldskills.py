import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import pandas as pd
import copy

def login():
    options = webdriver.ChromeOptions()
    
    options.add_argument('headless')
    options.add_argument('no-sandbox')
    
    options.add_argument('disable-gpu')
    options.add_argument('lang=ko_KR')
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(executable_path='./chrome_driver/chromedriver.exe' ,options=options)
    driver.get('https://meister.hrdkorea.or.kr/sub/11/1/1/login/login.do')
    
    driver.implicitly_wait(2)
    
    driver.find_element_by_name('mem_id').send_keys('마이스터넷 ID')
    driver.find_element_by_name('mem_pw').send_keys('마이스터넷 PW')
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[3]/div[3]/div/div/div/fieldset/div/form/a').click()
    
    driver.implicitly_wait(2)
    
    cookie_dict = {}
    
    for cookie in driver.get_cookies():
        cookie_dict[cookie['name']] = cookie['value']
    
    return cookie_dict['JSESSIONID']

def get_latest_data(session):
    
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    cookie = {'JSESSIONID':session}

    latest_data = list()

    for i in range(1,3):
        url = f'https://meister.hrdkorea.or.kr/sub/3/3/7/skillMatchTournament/taskQuestionsList.do?page={i}&searchKey=subject&searchValue=&competCode=2022P00&jobCode=337&mid=11&sid=1&tid=1'
        res = requests.get(url, headers=header, cookies=cookie)
        soup = BeautifulSoup(res.text, 'html.parser')

        tr = soup.select('#searchForm > div.introArea > table > tbody > tr')

        for j in tr:
            tmp = list()
            td = j.find_all('td')

            # print(len(td[2].get_text()))

            if len(td[2].get_text()):
                tmp.append(td[2].get_text())
                tmp.append('https://meister.hrdkorea.or.kr'+td[3].find('a')['href'])

                comment_count = re.sub(r'[^0-9]', '', td[3].get_text())

                if comment_count:
                    tmp.append(int(comment_count)) 
                else:
                    tmp.append(0)

                latest_data.append(tmp)

    return latest_data

def get_changed_data(latest_data):
    tmp = pd.read_csv('skills_data/data.csv')
    previous_data = tmp.values.tolist()

    changed_data = list()
    tmp = copy.deepcopy(latest_data)

    for i in range(len(previous_data)):
        latest = latest_data[i][2]
        preview = previous_data[i][2]

        if latest != preview:
            tmp[i].append(int(latest-preview))
            changed_data.append(tmp[i])

    df = pd.DataFrame(latest_data)
    df.to_csv('skills_data/data.csv', index=False)

    return changed_data

def result(changed_data):
    message = ''

    if len(changed_data):
        for i in changed_data:
            message += f'[{i[0]}] '

            if i[3] > 0:
                message += f'{i[3]}개의 댓글이 추가되었습니다. (현재: {i[2]}개)\n'
            else:
                message += f'{-i[3]}개의 댓글이 삭제되었습니다. (현재: {i[2]}개)\n'

            message += f'url: {i[1]}\n\n'

        return message

    else:
        return None


