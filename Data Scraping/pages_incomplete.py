from pickle import TRUE
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from wordcloud import WordCloud, STOPWORDS

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

browser=webdriver.Chrome("C:\\Users\\USER\\Documents\\chromedriver_win32\\chromedriver.exe",options=options)
browser.get("https://www.linkedin.com")

username=browser.find_element_by_id("session_key")
username.send_keys("username")
password=browser.find_element_by_id("session_password")
password.send_keys("password")

login_button=browser.find_element_by_class_name("sign-in-form__submit-button")
login_button.click()
browser.get("https://www.linkedin.com/jobs/search/?currentJobId=3219784412&geoId=104305776&keywords=cybersecurity&location=United%20Arab%20Emirates&refresh=true&sortBy=R")

job=browser.find_elements_by_class_name("job-card-list__title")

disc_list = []

for i in range(1, 5):
    browser.find_element_by_xpath(f'/html/body/div/div/div/div/div/main/div/section/div/div/ul/li[{i}]/button').click()
    time.sleep(2)
    
    jobs_lists = browser.find_element(By.CLASS_NAME,'jobs-search-results-list__text')  # here we create a list with jobs
    jobs = jobs_lists.find_elements(By.CLASS_NAME,'job-card-list__title')  # here we select each job to count
    
    time.sleep(2)
    
    c=[]
    # for i.text in job:
    #     #print(i.text)
    #     c.append(i.text)
    # print(c)
    # print()
    # print(len(c))

    job_title=[]
    for i in range(len(c)):
        job_title.append(c[i].strip("Job Title\n"))
        job_title
    print(job_title)

    job2=browser.find_elements_by_class_name("artdeco-entity-lockup__subtitle")
    comp_name=[]
    for j in job2:
        print(j.text)
        comp_name.append(j.text)
    print(comp_name)
    print()
    print(len(comp_name))

    job3 = browser.find_elements_by_class_name("job-card-container__metadata-wrapper")
    # class="job-card-container__metadata-item"

    loc_name=[]
    for j in job3:
        #print(i.text)
        loc_name.append(j.text)
    print(loc_name)
    print()
    print(len(loc_name))

    # jobs_lists = browser.find_element_by_class_name('jobs-search-results__list') #here we create a list with jobs
    jobs = browser.find_elements_by_class_name('job-card-list__title')#here we select each job to count
    jobs_lists = browser.find_element_by_class_name('jobs-search-results-list__text')
    time.sleep(1) 
    desc_list=[]
    
    for job in range (1, len(jobs)+1):
        browser.find_element_by_xpath(f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[5]/div/div[1]/div[1]/div[2]/div[1]/a').click()
        time.sleep(1)
        job_desc = browser.find_element_by_class_name('jobs-description-content__text')        
        soup = BeautifulSoup(job_desc.get_attribute('outerHTML'), 'html.parser')
        desc_list.append(soup.text)

    df = pd.DataFrame({"Description":desc_list})

df = df.replace(['\n',
                 '^.*?Expect', 
                 '^.*?Qualifications', 
                 '^.*?Required', 
                 '^.*?expected', 
                 '^.*?Responsibilities', 
                 '^.*?Requirements', 
                 '^.*?great', 
                 '^.*?Looking For', 
                 '^.*?ll Need', 
                 ], '', regex=True)

stopwords = set(STOPWORDS)
badwords = {'gender', 'experience', 'application', 'Apply', 'salary', 'todos', 'os', 'company', 'identity',
          'client','world', 'year', 'save','information','equal', 'oppotunity','will', 'national origin','work', 'years','clients', 'creating',
          'employer', 'working','data', 'people', 'one', 'knowledges', 'software', 'opportunity', 'solution', 'national', 'origin',
          'option', 'sicence', 'team','veteran', 'status', 'etc', 'Scientist','job', 'knowledge', 'toll', 'time', 'solutions', 'show', 'tool', 'regard', 
          'without', 'make','life', 'interested', 'proud', 'ability', 'options', 'using', 'product', 'building', 'skill', 'model', 
          'religion', 'Share', 'receive', 'consideration','Strong', 'Pay', 'range', 'available', 'part', 'employment', 'qualified', 'applicants', 
          'Yes', 'moment', 'new', 'Try', 'Premium', 'employee','unavailable', 'hiring', 'trends', 'recent',  'build', 'career', 
          'total', 'free', 'Full', 'Job', 'Description'}

stopwords.update(badwords)
print(df)

# fd=pd.DataFrame({"Company Name":comp_name,"Job Title":job_title,"Location":loc_name})
# list=[fd,df]

# result=pd.concat(list,axis=1)
# # print(df)
# print(result)
# # exporting our dataframe to a csv file
# df.to_csv('wordcloud-job.csv', sep=';')