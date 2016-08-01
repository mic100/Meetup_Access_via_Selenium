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
sa.send_keys("YOUR_LOGIN_HERE")

#Do the same thing for password and fill in.
sb = browser.find_element_by_name('password')
sb.send_keys('YOUR_PASSWORD_HERE')
sb.send_keys(Keys.RETURN)

urla = "YOUR_MEETUP_GROUP_URL_HERE"

actions = ActionChains(browser)
actions.move_to_element('Membres')
browser.find_element_by_xpath('//a[@href="%s"]' %(urla)).click()

#-----------------------------------------------------------------------------#

def action(browser, a, b) :
    
    actions = ActionChains(browser)
    actions.move_to_element(b)
    browser.find_element_by_xpath('//a[@href="%s"]' %(a)).click()
    time.sleep(3)

#-----------------------------------------------------------------------------#

def gsfh() :
    
    #get the html page.
    html = browser.page_source
    #parse the html page with bs4.
    soup = bs(html,'html.parser')
    return soup
    
#-----------------------------------------------------------------------------#

def get_mm_data(s='yes') :

    STATUS = s #STATUS (='no'(off),='yes'(on))   
    
    if STATUS == 'no' :
        pass
    elif STATUS == 'yes' :
        
        #get meetup member name and profile page url.
        g = gsfh().find_all('span', {'class' : 'memName fn'})[0].text
        print 'name :', g
        print 'profile_url :', browser.current_url, '\n'

        #get meetup members location.     
        a = gsfh().find_all('span', {'class' : 'locality'})
        location = a[1].text#.strip()
        print 'location :', location
    
        #get meetup members membership date.
        b = gsfh().find_all('div', {'class' : 'unit size1of3'})  
        gm_date = b[1].find_all('p')[0].text#.strip()
        print 'gm_date :', gm_date
        
        #get meetup members membership photo url.
        c = gsfh().find_all('img', {'class' : 'D_memberProfilePhoto photo big-preview-photo'})
        thumb_url = c[0].get('src')
        print 'thumb_url :', thumb_url
        
        #get meetup members common membership group name.
        d = gsfh().find_all('div', {'class' : 'figureset-description'})
        d1 = [i.find_all('a') for i in d] 
        cmgl = []
        for j in d1 :
            cmg = {}
            cmg['%s' %(j[0].text)] = j[0].get('href')
            cmgl.append(cmg)
        print 'common_group :', cmgl#, '\n'
        print 'common_group_num :', len(cmgl)
        
        #get meetup members other groups (all groups).
        e = gsfh().find_all('ul', {'id' : 'my-meetup-groups-list'})
        try : 
            e1 = [i.find_all('div', {'class' : 'D_name bold'}) for i in e][0]
            mogl = []
            for k in e1 :
                mog = {}
                k1 = k.find_all('a', {'class' : 'omnCamp omngj_pcg4'})[0]        
                mog['%s' %(k1.text)] = k1.get('href')
                mogl.append(mog)
            print 'other_group :', mogl#, '\n'
            print 'other_group_num', len(mogl)
        except : 
            mogl = []
            print 'other_group :', mogl#, '\n'
            print 'other_group_num :', len(mogl)
            
        #get meetup member personnal interests.
        f = gsfh().find_all('ul', {'id' : 'memberTopicList'})
        f1 = [i.find_all('a') for i in f][0]
        mpil = []
        for l in f1 :
            mpi = {}
            mpi[l.text] = l.get('href')
            mpil.append(mpi)
        print 'personnal_interests :', mpil#, '\n'
        print 'personnal_interests_num :', len(mpil)

#-----------------------------------------------------------------------------#

def get_mm(t=3) :
    
#    print 'current_url :', browser.current_url, '\n'
    h = gsfh().find_all('ul',{'id' : 'memberList'})[0]
    h = h.find_all('a', {'class' : 'memName'})
    
    mytext = "https://www.meetup.com/fr-FR/cultiver-autrement-des-legumes-a-paris/members/"
    item_list = []
#    print '\n', 'item_list :', len(item_list), item_list, '\n'
    
    for i in h : 
        d = {}
#        print '\n', 'd :', d
        x = i.get('href').replace(mytext,'').replace('/','').strip()
        y = i.text
        d['%s' %(x)]  = y
#        print 'd :', d, '\n'
        item_list.append(d)
        
#    print '\n', 'd :', d, '\n'
#    print 'item_list :', item_list
#    print '\n'
    
    for j in item_list :
        memnum = j.keys()[0]
        elem = j[memnum]
        link = "https://www.meetup.com/fr-FR/cultiver-autrement-des-legumes-a-paris/members/%s/" %(memnum)
#        print elem, link #VERIF LINE
        actions = ActionChains(browser)
        actions.move_to_element('%s' %(elem)) 
        browser.find_element_by_xpath('//a[@href="%s"]' %(link)).click()
        #use of gmm_data here to get members data like in the meetup API
        get_mm_data()
        browser.back()
        time.sleep(t)

#-----------------------------------------------------------------------------#

def main() :
    
    s2 = gsfh().find_all('li', {'class':'nav-pageitem'})
    
    pu = []
    
    for i in s2 :
        a = i.find_all('a')[0].get('href')
        b = i.find_all('a')[0].text
        
        if b == u'→'  or b == u'←' :
            pass
        elif b == u'10' :
    
#            print '\n', b, a, '\n'
            pu.append(a)
            action(browser=browser, a=a, b=b)
            get_mm(t=5)
            html1 = browser.page_source
            #parse the html page with bs4.
            soup2 = bs(html1,'html.parser')
            s3 = soup2.find_all('li', {'class':'nav-pageitem'})
            for i in s3 :
                a1 = i.find_all('a')[0].get('href')
                b1 = i.find_all('a')[0].text 
                
                if a1 not in pu :
#                    print '\n', b1, a1, '\n'
                    pu.append(a1)                
                    action(browser=browser, a=a1, b=b1)
                    get_mm(t=5)
                else :
                    pass
                
                if b1 == u'→'  or b == u'←' :
                    pass
                elif b1 == u'14' :
    
                    if a1 not in pu :
#                        print '\n', b1, a1, '\n'
                        pu.append(a1)                    
                        action(browser=browser, a=a1, b=b1)
                        get_mm(t=5)
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
#                            print '\n', b2, a2, '\n'
                            pu.append(a2)                        
                            action(browser=browser, a=a2, b=b2)
                            get_mm(t=5)
                        else :
                            pass                     
        else : 
#            print '\n', b, a, '\n'
            pu.append(a)
            action(browser=browser, a=a, b=b)
            get_mm(t=5)

#-----------------------------------------------------------------------------#

if __name__ == "__main__" :
    
    main()
    #pass
    
