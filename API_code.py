import os
import requests
from dotenv import load_dotenv
from db import save_job, init_database

load_dotenv()

def fetch_jobs(job_role):
    # Retrieve key cleanly inside the call
    rapid_api_key = os.getenv("API_KEY", "").strip()
    
    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "jsearch27.p.rapidapi.com"
    }

    url = "https://jsearch27.p.rapidapi.com/search"
    params = {
        "query": job_role.strip(),
        "page": "1",
        "num_pages": "1"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        job_data=response.json().get("data", [])
        save_job(job_data,job_role)
        descriptions = []
        for job in job_data:
            if isinstance(job, dict):
                # Get description text and make sure it is a string
                desc = job.get("job_description") or job.get("description") or ""
                if desc:
                    descriptions.append(str(desc))
            elif isinstance(job, str):
                descriptions.append(job)
                
        return descriptions
    else:
        print(f"API Error {response.status_code}: {response.text}")
        return []
























# #used for to get secret APi key in other file
# load_dotenv()
# rapid_api_key=os.getenv("API_KEY")
# #function to get required job list
# def fetch_jobs(job_role):
#     if not job_role:
#         return 0
#     init_database()
#     url="https://jsearch.p.rapidapi.com/search"
#     headers={
#         "X-api_key":rapid_api_key,
#         "X-api_host":"jsearch.p.rapidapi.com"
#     }
#     params={
#         "query": job_role.strip(),
#         "page": "1",
#         "num_pages": "2"
#     }
#     try:
#         response = requests.get(url, headers=headers, params=params) #response as a http client which go towards destination with these headers,url, and params
#         if response.status_code == 200:
#             job_data = response.json().get("data", []) #response.json converts data into dictionary from 
#             save_job(job_data, job_role)
#             return len(job_data)
#         else:
#             print(f"API Error {response.status_code}: {response.text}")
#             return 0
#     except Exception as e:
#         print(f"Network error while fetching jobs: {e}")
#         return 0

