import requests as re
from bs4 import BeautifulSoup as bs
import os







URL  = "https://www.kaggle.com"
respone = re.get(URL)

print("response -->",respone,"\ntype -->","type-->",type(respone))

print("response content -->",respone.content,"\ntext -->",respone.text,"\nstatus code -->",respone.status_code)


if respone.status_code != 200:
    print("HTTP connection not  successful")
else:
    print("HTTP connection successful") 


    soup = bs(respone.content,'html.parser')


    print("title with tags -->",soup.title,"\ntitle without tags -->",soup.title.text)

for link in soup.find_all("link"):
    print(link.get("href"))

    print(soup.get_text())




folder="mini dataset"

if not os.path.exists(folder):
    os.makedirs(folder)


def scrape_content(URL):
    response = re.get(URL)
    if response.status_code == 200:
        print(f"Successfully established the connection  {URL}")
        return response
    else:
        print(f"HTTPS connection not successful for the url   {URL}")

        return None
    

path = os.getcwd( ) + "/" + folder 

def save_HTML(to_where,text,name):
    with open(f"{to_where}/page_{name}.html","w",encoding="utf-8") as f:
        f.write(text)
    print(f"HTML page saved successfully at {to_where}/page_{name}.html")


urls = ["https://www.kaggle.com",
    "https://stackoverflow.com",
    "https://www.researchgate.net",
    "https://www.python.org",
    "https://www.w3schools.com",
    "https://wwwen.uni.lu",
    "https://github.com",
    "https://www.mendeley.com",
    "https://www.overleaf.com",
                ]

def create_mini_dataset(to_where, urls):
    for i in range(0, len(urls)):
        content = scrape_content(urls[i])
        if content is not None:
            save_HTML(to_where, content.text, str(i))
        else:
            pass
    print("Mini dataset created successfully")

create_mini_dataset(path, urls)