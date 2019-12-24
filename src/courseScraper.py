from bs4 import BeautifulSoup
import requests

allLinks = []
pageUrl = 'https://www.uoguelph.ca/registrar/calendars/undergraduate/current/c12/'

coursePage = requests.get(pageUrl)
coursePgContents = coursePage.content
soup = BeautifulSoup(coursePgContents, 'html.parser')

courseListDiv = soup.findAll('div', {'class': 'subnav'})

for a in courseListDiv:
    courseListAnchors = a.findAll('a', href=True)

courseListAnchors.pop(0)

for link in courseListAnchors:
    allLinks.append(link['href'][2:])
