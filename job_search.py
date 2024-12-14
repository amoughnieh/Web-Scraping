from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import re

def job_search():
    # remove trailing and leading quotes in case the search
    # term was entered as a string
    search_term_cleaned = search_term.strip(r'\'\"')
    driver = webdriver.Chrome()  # or webdriver.Firefox(), etc.

    st = '%20'.join(search_term_cleaned.split())
    url = f'https://www.upwork.com/nx/search/jobs/?nbs=1&per_page={num_results}&q={st}&sort=recency'
    driver.get(url)

    # get the page source after JavaScript rendering
    html_text = driver.page_source
    soup = BeautifulSoup(html_text, "lxml")

    # close the browser after collecting the data
    driver.quit()

    # Find jobs inside collected page content
    jobs = soup.find_all('article', class_="job-tile cursor-pointer px-md-4 air3-card air3-card-list px-4x")

    # obtain date and time to give file unique name
    date = datetime.today().strftime('%Y-%m-%d')
    time = datetime.today().strftime('%Hh-%Mm')

    # Extract information from jobs
    for j_no, job in enumerate(jobs):

        # if error arises it will move to the next job
        try:
            job_link = f'https://www.upwork.com{job.a["href"]}'
            job_title = job.find('a').text

            nl_patt = r'\n\n\n+'
            sp_patt = r'  +'

            job_description = re.sub(nl_patt, '\n\n', job.p.text) # any 3 or more new lines is replaced with 2 new lines.
            job_description = re.sub(sp_patt, ' ', job_description) # replace excessive spaces with single space.

            pay = ' - '.join([txt.text.strip() for txt in job.find('ul', class_='job-tile-info-list text-base-sm mb-4') if txt.text.strip()])

            title = f'Job {j_no+1}: {job_title}'
            title_border = ''.join(['#' for _ in range(len(title))])

            # save extracted job info
            with open(f'{date}, {time} - {search_term_cleaned} - job posts.txt', 'a', encoding='utf-8') as f:
                f.write(f'{title_border}\n')
                f.write(f'{title}\n')
                f.write(f'{title_border}\n')

                f.write(f'\n**Job description**\n{job_description}\n')
                f.write(f'\n**Pay**\n{pay}\n')
                f.write(f'\n**Job link**\n{job_link}\n\n')

        except Exception as e:
            print(f'Error processing a job {e}')

if __name__ == '__main__':
    print('Enter search term:')
    search_term = input('>')

    print('Enter desired number of returned results (10, 20, or 50 only):')
    num_results = input('>')

    print('Enter desired number of minutes before next check:')
    mins = input('>')

    while True:
        job_search()
        day_next = (datetime.now() + timedelta(minutes=int(mins))).strftime('%Y-%m-%d')
        mins_next = (datetime.now() + timedelta(minutes=int(mins))).strftime('%Hh:%Mm')
        print(f"Waiting {mins} minutes... Next search on {day_next} at {mins_next}")
        time.sleep(int(mins)*60)

