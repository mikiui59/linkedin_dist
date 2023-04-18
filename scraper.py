import json
import time
import random
from linkedin_scraper import Person,Company, actions
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager 
import pandas as pd
from tqdm import tqdm
import os

with open('./health-fitness.txt','r') as f:
    j=json.load(f)

company=[]
title=[]
for i in j:
    if 'company' in i.keys():
        company.append(i['company'])
    if 'title' in i.keys():
        title.append(i['title'])

        


chromedriver=ChromeDriverManager().install()

driver = webdriver.Chrome(chromedriver)

driver.get('https://www.linkedin.com/login')

run= input('Run:')

if os.path.isfile('company.json'):
    p=int(input("Json file found. Do you want to skip rescreping file (1 or 0): "))
else:
    p=0
if p==0:
    data=[]
    for i in tqdm(range(0,len(company))):
        try:
            url=f'https://www.linkedin.com/search/results/companies/?keywords={company[i]}'

            driver.get(url)
            time.sleep(1+random.randint(-1,4)/5)
            f=driver.find_elements_by_css_selector('span a.app-aware-link')

            if f!=[]:

                link=f[0].get_attribute('href')
                driver.get(link+'/people/')

                driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight));")
                time.sleep(2)

                button=driver.find_elements_by_css_selector('button.artdeco-button.artdeco-button--muted.artdeco-button--1.artdeco-button--full.artdeco-button--secondary.ember-view.scaffold-finite-scroll__load-button')
                if button!=[]:
                    while True:
                        button=driver.find_elements_by_css_selector('button.artdeco-button.artdeco-button--muted.artdeco-button--1.artdeco-button--full.artdeco-button--secondary.ember-view.scaffold-finite-scroll__load-button')
                        if button!=[]:
                            button[0].click()
                            time.sleep(2)
                            driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight));")
                        else:
                            break


                driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight));")
                time.sleep(1+random.randint(-1,4)/5)

                f0=driver.find_elements_by_css_selector('div.artdeco-entity-lockup__title.ember-view a.app-aware-link')
                if f0!=[]:

                    data.append({'i':i,'company':company[i],'url':link,'people':[l.get_attribute('href') for l in f0]})

            time.sleep(2+random.randint(-1,4)/5)
            #print(i)
        except Exception as e:
            print(i,e)

    with open("company.json", "w") as outfile:
        json.dump(data, outfile)

df=[]


for i in tqdm(range(0,len(data))):

    people=data[i]['people']

    for p in people:

        driver.get(p)

        name=driver.find_elements_by_css_selector('h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words')[0].text
        dist=driver.find_elements_by_css_selector('span span.dist-value')[0].text
        df.append({'company':data[i]['company'],'company_url':data[i]['url'],'name':name,'url':p,'dist':dist})

        time.sleep(1+random.randint(-1,4)/5)



d=pd.DataFrame(df)

d.to_csv('connections.csv')
