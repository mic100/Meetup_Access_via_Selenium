# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as bs
import time

url = "https://secure.meetup.com/fr-FR/login/?returnUri=https%3A%2F%2Fwww.meetup.com%2Ffr-FR%2Fcultiver-autrement-des-legumes-a-paris%2F"
browser = webdriver.Firefox()

browser.get(url)

#Enter e-mail adress to login and fill in.
sa = browser.find_element_by_name('email')
sa.send_keys("HERE_YOUR_LOGIN_TO_MEETUP.COM")

#Do the same thing for password and fill in.
sb = browser.find_element_by_name('password')
sb.send_keys('HERE_YOUR_PASSWORD_TO_MEETUP.COM')
sb.send_keys(Keys.RETURN)

urla = "https://www.meetup.com/fr-FR/cultiver-autrement-des-legumes-a-paris/members/"

actions = ActionChains(browser)
actions.move_to_element('Membres')
browser.find_element_by_xpath('//a[@href="%s"]' %(urla)).click()

#-----------------------------------------------------------------------------#

def action(browser, a, b) :
    actions = ActionChains(browser)
    actions.move_to_element(b)
    browser.find_element_by_xpath('//a[@href="%s"]' %(a)).click()
    time.sleep(3)
#    browser.back()
#    time.sleep(3)
#    print browser.current_url

#-----------------------------------------------------------------------------#

def gsfh() :
    
    #get the html page.
    html = browser.page_source
    #parse the html page with bs4.
    soup1 = bs(html,'html.parser')
    return soup1
    
#-----------------------------------------------------------------------------#

def gmm(origin=gsfh()) :
    
    h = origin.find_all('ul',{'id' : 'memberList'})[0]
    h = h.find_all('a', {'class' : 'memName'})
    
    mytext = "https://www.meetup.com/fr-FR/cultiver-autrement-des-legumes-a-paris/members/"
    item_list = []
    
    for i in h : 
        d = {}
        x = i.get('href').replace(mytext,'').replace('/','').strip()
        y = i.text
        d['%s' %(x)]  = y
        item_list.append(d)
    
    print '\n'
    
    for j in item_list :
        memnum = j.keys()[0]
        elem = j[memnum]
        link = "https://www.meetup.com/fr-FR/cultiver-autrement-des-legumes-a-paris/members/%s/" %(memnum)
        print elem, link
        actions = ActionChains(browser)
        actions.move_to_element('%s' %(elem)) 
        browser.find_element_by_xpath('//a[@href="%s"]' %(link)).click()
        browser.back()
        time.sleep(3)


#-----------------------------------------------------------------------------#

s2 = gsfh().find_all('li', {'class':'nav-pageitem'})

pu = []

for i in s2 :
    a = i.find_all('a')[0].get('href')
    b = i.find_all('a')[0].text
    
    if b == u'→'  or b == u'←' :
        pass
    elif b == u'10' :

        print '\n', b, a
        pu.append(a)
        action(browser, a, b)
        gmm()
        html1 = browser.page_source
        #parse the html page with bs4.
        soup2 = bs(html1,'html.parser')
        s3 = soup2.find_all('li', {'class':'nav-pageitem'})
        for i in s3 :
            a1 = i.find_all('a')[0].get('href')
            b1 = i.find_all('a')[0].text 
            
            if a1 not in pu :
                print '\n', b1, a1
                pu.append(a1)                
                action(browser, a1, b1)
                gmm()
            else :
                pass
            
            if b1 == u'→'  or b == u'←' :
                pass
            elif b1 == u'14' :

                if a1 not in pu :
                    print '\n', b1, a1
                    pu.append(a1)                    
                    action(browser, a1, b1)
                    gmm()
                else :
                    pass
                
                html2 = browser.page_source
                #parse the html page with bs4.
                soup3 = bs(html2,'html.parser')
                s4 = soup3.find_all('li', {'class':'nav-pageitem'})
                for i in s4 :
                    a2 = i.find_all('a')[0].get('href')
                    b2 = i.find_all('a')[0].text 
                    
                    if a2 not in pu :
                        print '\n', b2, a2
                        pu.append(a2)                        
                        action(browser, a2, b2)
                        gmm()
                    else :
                        pass                    
        
    else : 
        print '\n', b, a
        pu.append(a)
        action(browser, a, b)
        gmm()

#-----------------------------------------------------------------------------#

#s2 = soup1.find_all('li', {'class':'nav-pageitem'})
#
#for i in s2 :
#    a = i.find_all('a')[0].get('href')
#    b = i.find_all('a')[0].text 
#    print b, a
#    actions = ActionChains(browser)
#    actions.move_to_element(b)
#    browser.find_element_by_xpath('//a[@href="%s"]' %(a)).click()
#    time.sleep(2)
#    browser.back()
#    time.sleep(3)
##    print browser.current_url
#
#html = browser.page_source
#soup2 = bs(html,'html.parser')
