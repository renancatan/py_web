import requests
import pandas as pd

BASE_URL = 'https://www.workingnomads.com/jobsapi/_search'
SEARCH = "Development"  # THE SEARCH CAN BE REMOVED
SEARCH_OPTIONS = "AND"

params = {
    'sort': 'premium:desc,pub_date:desc',
    '_source': ",".join([
        "company", "company_slug", "category_name", "description", "locations",
        "location_base", "salary_range", "salary_range_short", "number_of_applicants",
        "instructions", "id", "external_id", "slug", "title", "pub_date",
        "tags", "source", "apply_option", "apply_email", "apply_url",
        "premium", "expired", "use_ats", "position_type"
    ]),
    'size': 100,
    'from': 0,
    'q': f'(category_name.raw:"{SEARCH}") {SEARCH_OPTIONS} (locations:"Anywhere")'  # OPTIONAL
}
headers = {
    'authority': 'www.workingnomads.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/116.0.0.0 Safari/537.36',
}

response = requests.get(BASE_URL, params=params, headers=headers)
status_code = response.status_code
raw_jobs = response.json()

df_jobs = pd.json_normalize(raw_jobs["hits"]["hits"])
df_jobs.to_csv("nomads.csv", encoding="utf-8")

filter_keyword = df_jobs[df_jobs['_source.description'].str.lower().str.contains('python', case=False, na=False)]
filter_keyword.to_csv("nomads_pythonJobs.csv", encoding="utf-8")
print(df_jobs, filter_keyword)


