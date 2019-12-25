from bs4 import BeautifulSoup
import requests
import pandas as pd

def courseScraper():
    allLinks = []
    allCourseTitles = []
    allCourseRestrictions = []
    allCoursePrerequisites = []
    allCourseCredits = []

    pageUrl = 'https://www.uoguelph.ca/registrar/calendars/undergraduate/current/c12/'

    coursePage = requests.get(pageUrl)
    coursePgContents = coursePage.content
    soup = BeautifulSoup(coursePgContents, 'html.parser')
    courseListDiv = soup.findAll('div', {'class': 'subnav'})

    for a in courseListDiv:
        courseListAnchors = a.findAll('a', href = True)

    courseListAnchors.pop(0)    # Getting rid of index.shtml

    for link in courseListAnchors:
        allLinks.append(link['href'][2:])

    for link in allLinks:
        coursePageUrl = pageUrl + link
        page = requests.get(coursePageUrl)
        contents = page.content
        courseSoup = BeautifulSoup(contents, 'html.parser')
        courseDivs = courseSoup.find_all('div', {'class': 'course'})
        
        for a in courseDivs:
            course = a.find('tr', {'class': 'title'}).get_text()
            courseTitle = course.split()[0]
            courseCredit = course.split()[-1][1:5]

            if a.find('tr', {'class': 'restrictions'}):
                restrictions = a.find('tr', {'class': 'restrictions'}).get_text().strip().replace('Restriction(s):', '').replace('\n', '')
            else:
                restrictions = "None"
            
            if a.find('tr', {'class': 'prereqs'}):
                prereq = a.find('tr', {'class': 'prereqs'}).get_text().strip().replace('Prerequisite(s):', '').replace('\n','')
            else:
                prereq = "None"
            
            allCourseTitles.append(courseTitle)
            allCourseCredits.append(courseCredit)
            allCoursePrerequisites.append(prereq)
            allCourseRestrictions.append(restrictions)
    
    courseData = pd.DataFrame(
        {'Course Title': allCourseTitles,
        'Course Credit': allCourseCredits,
        'Course Prerequisites': allCoursePrerequisites,
        'Course Restrictions': allCourseRestrictions
        }
    )
    courseData.to_csv('courseData.csv')

courseScraper()
