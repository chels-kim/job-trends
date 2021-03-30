import requests
from bs4 import BeautifulSoup
import spacy
from spacy.matcher import PhraseMatcher

# Perform basic job search
root_URL = 'https://ca.indeed.com'
URL = '/jobs?q=data+scientist&l=Toronto%2C+ON'
page = requests.get(root_URL + URL)

# parse HTML using Beautiful Soup
page_soup = BeautifulSoup(page.content, 'html.parser')
page_results = page_soup.find(id='resultsCol')
job_elems = page_results.find_all('div', class_='jobsearch-SerpJobCard unifiedRow row result')

# Find links to each job posting
jobs = {}
job_requirement_keys = ['require', 'experience', 'skill']

for job_elem in job_elems[0:3]:
    title_elem = job_elem.find('h2', class_='title')
    job_title = title_elem.find('a', class_='jobtitle').text.strip()
    company = job_elem.find('span', class_='company').text.strip()
    location = job_elem.find('span', class_='location').text.strip()

    post_URL = root_URL + title_elem.find('a')['href']

    post = requests.get(post_URL)
    post_soup = BeautifulSoup(post.content, 'html.parser')
    post_date = post_soup.find('div', class_='jobsearch-JobMetadataFooter').find('div', class_=None).text

    post_details = post_soup.find('div', class_='jobsearch-jobDescriptionText').\
        find(string=lambda text: any(key in text.lower() for key in job_requirement_keys))
    print(post_details)


    # if None in (title_elem, company_elem, location_elem):
    #     continue

