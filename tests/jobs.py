from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import smtplib
from email.message import EmailMessage


"""Remote URLs"""
remote_developer_url = 'https://www.google.com/search?q=developer&hl=en&ibp=htl;jobs&sa=X&ved=2ahUKEwidyJbYuKr3AhXCIUQIHUy9Bw4QutcGKAF6BAgEEAY&sxsrf=APq-WBsRTt1ySgTuS1BnsvMawJPUXrjx8A:1650725767986#fpstate=tldetail&htivrt=jobs&htichips=requirements:no_experience,requirements:years3under,employment_type:FULLTIME,employment_type:CONTRACTOR&htischips=requirements;no_experience;years3under,employment_type;FULLTIME;CONTRACTOR&htiltype=1'
remote_software_url = 'https://www.google.com/search?q=software&hl=en&ibp=htl;jobs&sa=X&ved=2ahUKEwidyJbYuKr3AhXCIUQIHUy9Bw4QutcGKAF6BAgEEAY&sxsrf=APq-WBsRTt1ySgTuS1BnsvMawJPUXrjx8A:1650725767986#fpstate=tldetail&htivrt=jobs&htichips=requirements:no_experience,requirements:years3under,employment_type:FULLTIME,employment_type:CONTRACTOR&htischips=requirements;no_experience;years3under,employment_type;FULLTIME;CONTRACTOR&htiltype=1'
remote_python_url = 'https://www.google.com/search?q=python&hl=en&ibp=htl;jobs&sa=X&ved=2ahUKEwidyJbYuKr3AhXCIUQIHUy9Bw4QutcGKAF6BAgEEAY&sxsrf=APq-WBsRTt1ySgTuS1BnsvMawJPUXrjx8A:1650725767986#fpstate=tldetail&htivrt=jobs&htichips=requirements:no_experience,requirements:years3under,employment_type:FULLTIME,employment_type:CONTRACTOR&htischips=requirements;no_experience;years3under,employment_type;FULLTIME;CONTRACTOR&htiltype=1'
remote_data_url = 'https://www.google.com/search?q=data&hl=en&ibp=htl;jobs&sa=X&ved=2ahUKEwidyJbYuKr3AhXCIUQIHUy9Bw4QutcGKAF6BAgEEAY&sxsrf=APq-WBsRTt1ySgTuS1BnsvMawJPUXrjx8A:1650725767986#fpstate=tldetail&htivrt=jobs&htichips=requirements:no_experience,requirements:years3under,employment_type:FULLTIME,employment_type:CONTRACTOR&htischips=requirements;no_experience;years3under,employment_type;FULLTIME;CONTRACTOR&htiltype=1'
remote_video_url = 'https://www.google.com/search?q=video&hl=en&ibp=htl;jobs&sa=X&ved=2ahUKEwidyJbYuKr3AhXCIUQIHUy9Bw4QutcGKAF6BAgEEAY&sxsrf=APq-WBsRTt1ySgTuS1BnsvMawJPUXrjx8A:1650725767986#fpstate=tldetail&htivrt=jobs&htichips=requirements:no_experience,requirements:years3under,employment_type:FULLTIME,employment_type:CONTRACTOR&htischips=requirements;no_experience;years3under,employment_type;FULLTIME;CONTRACTOR&htiltype=1'

"""Santa Monica URLs"""
santa_monica_developer_url = 'https://www.google.com/search?q=php+developer+London+CA&hl=en&ibp=htl;jobs&sa=X&ved=2ahUKEwidyJbYuKr3AhXCIUQIHUy9Bw4QutcGKAF6BAgEEAY&sxsrf=APq-WBsRTt1ySgTuS1BnsvMawJPUXrjx8A:1650725767986#fpstate=tldetail&htivrt=jobs&htichips=city:GQCRws6kwoCr9SP_tQoXtA%3D%3D,requirements:no_experience,requirements:years3under,employment_type:FULLTIME,employment_type:CONTRACTOR&htischips=city;GQCRws6kwoCr9SP_tQoXtA%3D%3D:Santa%20Monica,requirements;no_experience;years3under,employment_type;FULLTIME;CONTRACTOR&htidocid=ZFrWzGNHDZMAAAAAAAAAAA%3D%3D'
santa_monica_software_url = 'https://www.google.com/search?q=laravel+developer+London+UK&hl=en&ibp=htl;jobs&sa=X&ved=2ahUKEwidyJbYuKr3AhXCIUQIHUy9Bw4QutcGKAF6BAgEEAY&sxsrf=APq-WBsRTt1ySgTuS1BnsvMawJPUXrjx8A:1650725767986#fpstate=tldetail&htivrt=jobs&htichips=city:GQCRws6kwoCr9SP_tQoXtA%3D%3D,requirements:no_experience,requirements:years3under,employment_type:FULLTIME,employment_type:CONTRACTOR&htischips=city;GQCRws6kwoCr9SP_tQoXtA%3D%3D:Santa%20Monica,requirements;no_experience;years3under,employment_type;FULLTIME;CONTRACTOR&htidocid=ZFrWzGNHDZMAAAAAAAAAAA%3D%3D'
santa_monica_python_url = 'https://www.google.com/search?q=symfony+developer+London+UK&hl=en&ibp=htl;jobs&sa=X&ved=2ahUKEwidyJbYuKr3AhXCIUQIHUy9Bw4QutcGKAF6BAgEEAY&sxsrf=APq-WBsRTt1ySgTuS1BnsvMawJPUXrjx8A:1650725767986#fpstate=tldetail&htivrt=jobs&htichips=city:GQCRws6kwoCr9SP_tQoXtA%3D%3D,requirements:no_experience,requirements:years3under,employment_type:FULLTIME,employment_type:CONTRACTOR&htischips=city;GQCRws6kwoCr9SP_tQoXtA%3D%3D:Santa%20Monica,requirements;no_experience;years3under,employment_type;FULLTIME;CONTRACTOR&htidocid=ZFrWzGNHDZMAAAAAAAAAAA%3D%3D'

"""Variables"""
jobs = {
    'remote': {
        'developer': {},
        'software': {},
        'python': {},
        'laravel': {},
        'data': {},
        'video': {},
    },
    'austin': {
        'developer': {},
        'software': {},
        'python': {},
        'data': {},
        'video': {},
    },
}

num = 1
urls = {
    'remote': [remote_developer_url, remote_software_url, remote_python_url, remote_data_url, remote_video_url],
    'London': [santa_monica_developer_url, santa_monica_software_url, santa_monica_python_url, santa_monica_data_url, santa_monica_video_url],
}
url_locations = ['remote', 'london']
url_categories = ['developer', 'php', 'laravel', 'symfony', 'python']

driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'))

for location in url_locations:
    n = 0
    for url in urls[location]:

        driver.get(url)
        time.sleep(5)

        postings = driver.find_elements(By.TAG_NAME, 'li')[0:5]
        time.sleep(1)

        cat = url_categories[n]

        for post in postings:
            post.click()
            time.sleep(0.5)

            job_section = driver.find_element(By.CLASS_NAME, 'whazf')
            job_title = job_section.find_element(By.TAG_NAME, 'h2')
            company_name = job_section.find_element(By.CLASS_NAME, 'nJlQNd')
            where = job_section.find_elements(By.CLASS_NAME, 'sMzDkb')
            link_tag = driver.find_element(By.PARTIAL_LINK_TEXT, 'Apply')
            link = link_tag.get_attribute('href')

            jobs[str(location)][str(cat)][str(num)] = {
                'title': job_title.text,
                'company': company_name.text,
                'location': where[1].text,
                'link': link,
            }

            time.sleep(0.5)
            if num >= 5:
                num = 0
            num += 1
        n += 1
print(jobs)

driver.quit()

'''send email with jobs'''
body = ''
for location in url_locations:
    new_loc_txt = f"{location.title()}\n\n"
    body += new_loc_txt
    for category in url_categories:
        new_cat_txt = f"    {category.title()}\n"
        body += new_cat_txt
        for n in range(1, 6):
            new_job_txt = f"        Title: {jobs[location][category][str(n)]['title']}\n" \
                          f"            Company: {jobs[location][category][str(n)]['company']}\n" \
                          f"            Where: {jobs[location][category][str(n)]['location']}\n" \
                          f"            link: {jobs[location][category][str(n)]['link']}\n\n"
            body += new_job_txt

print(body)

to_email_address = 'bogdan.izdrail@gmail.com'
from_email_address = 'derekdummytest@gmail.com'
password = 'dddeeerrreeekkk'
today = datetime.today().strftime('%Y-%m-%d')

msg = f"""From: {from_email_address}
To: {to_email_address}
Subject: Current Job Openings - {today}\n
{body}
"""

server = smtplib.SMTP_SSL('smtp.gmail.com', port=465)
server.set_debuglevel(1)
server.ehlo
server.login(from_email_address, password)
server.sendmail(from_email_address, to_email_address, msg)
server.quit()
