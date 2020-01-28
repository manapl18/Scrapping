from bs4 import BeautifulSoup
import requests

LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=it&l=%EB%B6%80%EC%82%B0%EA%B4%91%EC%97%AD%EC%8B%9C&limit={LIMIT}"
company_URL = f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?"

def extract_indeed_page():
    result = requests.get(f"{URL}")
    soup = BeautifulSoup(result.text,"html.parser")

    pagination = soup.find("div",{"class":"pagination"})

    links = pagination.find_all("a")
    spans = []
    for link in links[:-1]:
        spans.append((int)(link.find("span").string))
    max_page = spans[-1]
    return max_page

def extract_indeed_job(result):
    title = result.find("a")["title"]
    company_title = result.find("span",{"class":"company"})
    company_anchor = company_title.find("a")
    company_location = result.find("div",{"class":"recJobLoc"})["data-rc-loc"]
    company_link = result.find("a")["id"]
    company_link = company_link[3:]
    if company_anchor is not None:
        company = str(company_anchor.string)
    else:
        company = str(company_title.string)
    company = company.strip()
    return {"title":title,"company":company,"location":company_location,"link":company_URL+f"jk={company_link}"}

def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{URL}&start={page*50}")
        page_result = BeautifulSoup(result.text,"html.parser")
        results = page_result.find_all("div",{"class":"jobsearch-SerpJobCard"})
        for result in results:
            job = extract_indeed_job(result)
            jobs.append(job)
    for result in jobs:
        print(result)

def get_jobs():
    extract_indeed_jobs(extract_indeed_page())