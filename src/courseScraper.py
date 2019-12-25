from bs4 import BeautifulSoup
import requests
import pandas as pd

def courseScraper():
    allLinks = []   # List to hold all anchor links for all courses
    allCourseTitles = []    # List to hold all course titles that needs to be transferred to the csv file
    allCourseRestrictions = []  # List to hold all course restrictions that needs to be transferred to the csv file
    allCoursePrerequisites = [] # List to hold all course Prerequisites that needs to be transferred to the csv file
    allCourseCredits = []   # List to hold all course credits that needs to be transferred to the csv file

    pageUrl = 'https://www.uoguelph.ca/registrar/calendars/undergraduate/current/c12/'

    coursePage = requests.get(pageUrl)
    coursePgContents = coursePage.content
    soup = BeautifulSoup(coursePgContents, 'html.parser')
    courseListDiv = soup.findAll('div', {'class': 'subnav'})

    # Getting all anchor tags from Accounting to Zoology
    for a in courseListDiv:
        courseListAnchors = a.findAll('a', href = True)

    courseListAnchors.pop(0)    # Getting rid of index.shtml

    # Getting all the extensions to go from Accounting to Zoology
    for link in courseListAnchors:
        allLinks.append(link['href'][2:])

    # Collecting all the course data from Accounting to Zoology
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
    
    # Sending in the collected data to the csv file
    courseData = pd.DataFrame(
        {'Course Title': allCourseTitles,
        'Course Credit': allCourseCredits,
        'Course Prerequisites': allCoursePrerequisites,
        'Course Restrictions': allCourseRestrictions
        }
    )
    courseData.to_csv('courseData.csv', encoding='utf-8',index=False)

courseScraper()
