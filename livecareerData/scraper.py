import requests as r
from lxml import html
from bs4 import BeautifulSoup
from math import ceil
from time import sleep
import concurrent.futures
import os
GTK_FOLDER = r'C:\Program Files\GTK3-Runtime Win64\bin'
os.environ['PATH'] = GTK_FOLDER + os.pathsep + os.environ.get('PATH', '')
import weasyprint

# bug when the job title is lawyer
class livecareerResumeUtill():

    def __init__(self, job_title):
        self.counter = 1
        # self.number_of_cvs = number_of_cvs + self.counter - 1
        self.job_title = job_title
        self.base_url = "https://www.livecareer.com"
        self.headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        self.retry_limit = 3
        self.retry_delay = 5  # seconds

    def fetch(self):
        url = self.base_url + "/resume-search/search?jt=" + self.job_title.replace(" ", "%20")
        print(url)
        
        for attempt in range(self.retry_limit):
            try:
                page = r.get(url, headers={'User-Agent': self.headers})
                tree = html.fromstring(page.content)
                break  # Exit the loop if request is successful
            
            except r.exceptions.ConnectionError as e:
                if attempt < self.retry_limit - 1:
                    print(f"Connection failed. Retrying in {self.retry_delay} seconds...")
                    sleep(self.retry_delay)
                else:
                    print("Failed to establish a connection after several attempts.")
                    # Handle the failed case (log, use fallback, etc.)  
                    return 
                
        print('----------------------------------------------------------------------------------------------------')
        
        # Ensure parent folder exists
        parent_folder = 'resume'
        job_folder = os.path.join(parent_folder, self.job_title)
        if not os.path.exists(parent_folder):
            os.mkdir(parent_folder)

        # Check and create job title folder inside parent folder
        if not os.path.exists(job_folder):
            os.mkdir(job_folder)


        links = tree.xpath("//*[@id='__next']/div[2]/div/div[3]/div[1]/a/@href")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.download, self.base_url + link) for link in links]
            for future in concurrent.futures.as_completed(futures):
                print(future.result())
            
    def download(self, link):
        print(link)
         
        for attempt in range(self.retry_limit):
            try:
                page = r.get(link, headers={'User-Agent': self.headers}, stream=True)
                # Process response here
                soup = BeautifulSoup(page.text, 'html.parser') 
                break  # Exit the loop if request is successful
            except r.exceptions.ConnectionError as e:
                if attempt < self.retry_limit - 1:
                    print(f"Connection failed. Retrying in {self.retry_delay} seconds...")
                    sleep(self.retry_delay)
                else:
                    print("Failed to establish a connection after several attempts.")
                    # Handle the failed case (log, use fallback, etc.)  
                    return 
        try:
            soup.find('body').contents = soup.find('div', {'id':'server-resume-template'}).contents

            with open("f.html", 'w') as f:
                f.write(str(soup.contents[1]))
            with open("f.html", 'rb') as f:
                pdf = weasyprint.HTML(f).write_pdf()
            file_ = os.path.join('resume', self.job_title, f"{self.counter}.pdf")
            print(file_)
            with open(file_, 'wb') as f:    
                f.write(pdf)

            self.counter+=1

        except:
            print('ERROR going to next')

        

# if __name__=="__main__":
#     x=livecareerResumeUtill("Data Scientist")
#     print(x.fetch())