'''
Logs on to the University of London's Endangered Language Archive (ELAR), and obtains the links
to individual packages archive's repository of the Chirag language.
'''


import mechanize
import pickle


username = '<username>'
password = '<password>'

loginPage = 'https://elar.soas.ac.uk/MyResearch/UserLogin'
home = 'https://elar.soas.ac.uk'

def extract_link(page, links):
    # links = {}
    while 'Chirag0' in page:
        page = page[page.find('Chirag0'):]
        quote = page.find('"')
        index = page[:quote]
        # print('\n Found index', index)
        page = page[page.find('href="')+6:]
        link = page[:page.find('"')]
        # print('\nFound link', link)
        links[index] = link

        for i in range(3):
            page = page[page.find('Chirag0')+10:]
    return links

def save_page(page):
    # print('Saving page...')
    page_out = open('Language Project/page.html', 'wb')
    page_out.write(page)
    page_out.close()
    # print('Done.')

def read_page():
    page_io = open('Language Project/page.html', 'r')
    page = page_io.read()
    page_io.close()
    return page

# Log in.
browser = mechanize.Browser()
browser.set_handle_robots(False)
browser.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]
print('Logging in...')
browser.open(loginPage)
browser.select_form(nr=1)
browser['username'] = username
browser['password'] = password
response_login = browser.submit()
print('Logged in.') #Assuming the attempt to log in always works.

print('Processing first page.')
links_io = open('Language Project/links.pickle', '+rb')
links = pickle.load(links_io)
links_io.close()
home_page = browser.open('https://elar.soas.ac.uk/Collection/MPI971094?type=AllFields&filter%5B%5D=NOT+deletion_message%3A%22deleted%22&filter%5B%5D=resource_access_protocol%3A%22U%22&dfApplied=1#items')
page_index = 1
page_content = home_page.read()
save_page(page_content)
page_content = read_page()

# while 'Next' in page_content:
for i in range(14): #Because the 'transcribed and translated' entries stop at page 14.
    print(len(links.keys()), ' Links before extraction: ', links.keys())
    links = extract_link(page_content, links)
    print(len(links.keys()), ' Links after extraction: ', links.keys())

    page_index += 1
    print('\n About to work on Page', page_index)
    print('Loading page...')
    response = browser.follow_link(text_regex=r"Next", nr=0)
    print('Page loaded.')
    page_content = response.read()
    save_page(page_content)
    page_content = read_page()


print('Saving links to file...')
links_io = open('Language Project/links.pickle', '+rb')
pickle.dump(links, links_io)
links_io.close()
print('Saved.')
