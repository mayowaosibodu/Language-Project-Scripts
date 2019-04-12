'''
Logs on to the University of London's Endangered Language Archive (ELAR).
Follows the list of links saved into links.pickle by crawler.py.
In these new pages, downloads the first file beginning with "Chirag0"
(Usually Chirag0XXX.eaf, the needed transcription files).

'''



import mechanize
import pickle


username = '<username>'
password = '<password>'
loginPage = 'https://elar.soas.ac.uk/MyResearch/UserLogin'
home = 'https://elar.soas.ac.uk'

def save_page(page):
    print('Saving page...')
    page_out = open('Language Project/page.html', 'wb')
    page_out.write(page)
    page_out.close()
    print('Done.')


#Log in.
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

#Unpickle links.
links_io = open('Language Project/links.pickle', '+rb')
links = pickle.load(links_io)
links_io.close()


for link in links:
# for link in ['Chirag0063']:
    if link != 1:
        address = home+links[link]
        recordPage = browser.open(address)
        recordPageContent = recordPage.read()
        save_page(recordPageContent)

        print('Saving file: ', link.lower())
        response = browser.follow_link(text_regex=link.lower(), nr=0) #This actually just follows the first link with the record name:chirag0XXX - in these cases Chirag 0XXX.eaf as is desired. Sometimes. I ended up unintentionaly downloading some pretty hefty WAV files.
        eaf_io = open('Language Project/Chirag Data/Annotations/'+link.lower()+'.eaf', 'wb')
        eaf_io.write(response.read())
        eaf_io.close()
        print('Done')
