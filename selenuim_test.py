# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------#

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as bs
import time
import os
import datetime

#-----------------------------------------------------------------------------#

#text file connection. 
def txt_wd(YOUR_DIRECTORY_TO_SAVE_DATA, data) :
    
    rep_dir= YOUR_DIRECTORY_TO_SAVE_DATA
    book_name = '%s.txt' %(data[0]['name'])
    
    if os.path.exists(rep_dir) :
        #save of .txt file to directory.        
        file = open(rep_dir + book_name, 'w')
        file.write(str(data))
        file.close() 
    else : 
        print 'Create folder', rep_dir, '\n'
        #create folder if not exist.
        os.mkdir(rep_dir)
        #save .txt file to directory.
        file = open(rep_dir + book_name, 'w')
        file.write(str(data))
        file.close()         
        
#-----------------------------------------------------------------------------#

#doing stuff with browser - click on link to go to the page -sleep 3 seconds.
def action(browser, a, b) :
    
    actions = ActionChains(browser)
    actions.move_to_element(b)
    browser.find_element_by_xpath('//a[@href="%s"]' %(a)).click()
    time.sleep(3)
#
#-----------------------------------------------------------------------------#

def gsfh(browser) :
    
    #get the html page.
    html = browser.page_source
    #parse the html page with bs4.
    soup = bs(html,'html.parser')
    return soup
    
#-----------------------------------------------------------------------------#

def get_mm_data(YOUR_DIRECTORY_TO_SAVE_DATA, browser, s='yes') :

    STATUS = s #STATUS (='no'(off),='yes'(on))   
    
    if STATUS == 'no' :
        pass
    elif STATUS == 'yes' :
        
        dict1, dict2, dict3, dict4, dict5, dict6, dict7, dict8, dict9, \
        dict10, dict11 = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}

        #get meetup member name and profile page url.
        g = gsfh(browser).find_all('span', {'itemprop' : 'name'})[0].text
        dict1['name'] = g.lower()
        dict2['profile_url'] = browser.current_url

        #get meetup members location.     
        a = gsfh(browser).find_all('span', {'class' : 'locality'})
        location = a[1].text#.strip()
        dict3['location'] = location
    
        #get meetup members membership date.
        b = gsfh(browser).find_all('div', {'class' : 'unit size1of3'})  
        gm_date = b[1].find_all('p')[0].text#.strip()
        dict4['gm_date'] = gm_date
        
        #get meetup members membership photo url.
        c = gsfh(browser).find_all('img', {'class' : 'D_memberProfilePhoto photo big-preview-photo'})
        thumb_url = c[0].get('src')
        dict5['thumb_url'] = thumb_url
        
        #get meetup members common membership group name.
        d = gsfh(browser).find_all('div', {'class' : 'figureset-description'})
        d1 = [i.find_all('a') for i in d] 
        cmgl = []
        for j in d1 :
            cmg = {}
            cmg['%s' %(j[0].text)] = j[0].get('href')
            cmgl.append(cmg)
        dict6['common_group'] = cmgl
        dict7['common_group_num'] = len(cmgl)
        
        #get meetup members other groups (all groups).
        e = gsfh(browser).find_all('ul', {'id' : 'my-meetup-groups-list'})
        try : 
            e1 = [i.find_all('div', {'class' : 'D_name bold'}) for i in e][0]
            mogl = []
            for k in e1 :
                mog = {}
                k1 = k.find_all('a', {'class' : 'omnCamp omngj_pcg4'})[0]        
                mog['%s' %(k1.text)] = k1.get('href')
                mogl.append(mog)
            dict8['other_group'] = mogl
            dict9['other_group_num'] = len(mogl)
        except : 
            mogl = []
            dict8['other_group'] = mogl
            dict9['other_group_num'] = len(mogl)
            
        #get meetup member personnal interests.
        f = gsfh(browser).find_all('ul', {'id' : 'memberTopicList'})
        f1 = [i.find_all('a') for i in f][0]
        mpil = []
        for l in f1 :
            mpi = {}
            mpi[l.text] = l.get('href')
            mpil.append(mpi)
        dict10['personnal_interests'] = mpil
        dict11['personnal_interests_num'] = len(mpil)
        
        #get all dict in a data list.
        data_dict = [dict1, dict2, dict3, dict4, dict5, dict6, dict7, dict8, dict9, \
                dict10, dict11]
             
        #write data to excel file.
        txt_wd(YOUR_DIRECTORY_TO_SAVE_DATA, data=data_dict)
                
        return data_dict

#-----------------------------------------------------------------------------#

def get_mm(YOUR_MEETUP_GROUP_URL_HERE, YOUR_DIRECTORY_TO_SAVE_DATA, browser, t=3) :
    
    h = gsfh(browser).find_all('ul',{'id' : 'memberList'})[0]
    h = h.find_all('a', {'class' : 'memName'})
    
    mytext = YOUR_MEETUP_GROUP_URL_HERE
    item_list = []
    
    for i in h : 
        d = {}
        x = i.get('href').replace(mytext,'').replace('/','').strip()
        y = i.text
        d['%s' %(x)]  = y
        item_list.append(d)

    for j in item_list :
        memnum = j.keys()[0]
        elem = j[memnum]
        link = YOUR_MEETUP_GROUP_URL_HERE + "%s/" %(memnum)
        actions = ActionChains(browser)
        actions.move_to_element('%s' %(elem)) 
        browser.find_element_by_xpath('//a[@href="%s"]' %(link)).click()
        #use of gmm_data here to get members data like in the meetup API
        #get meetup members data and write it to :
        #excel file
        get_mm_data(YOUR_DIRECTORY_TO_SAVE_DATA, browser)
        browser.back()
        time.sleep(t)

#-----------------------------------------------------------------------------#

def main(YOUR_DIRECTORY_TO_SAVE_DATA, YOUR_MEETUP_LOGIN_GROUP_URL_HERE, \
    YOUR_MEETUP_GROUP_URL_HERE, YOUR_MEETUP_LOGIN_NAME_HERE, \
    YOUR_MEETUP_PASSWORD_HERE) :

    url = YOUR_MEETUP_LOGIN_GROUP_URL_HERE 
    browser = webdriver.Firefox()
    browser.get(url)
    
    #Enter e-mail adress to login and fill in.
    sa = browser.find_element_by_name('email')
    sa.send_keys(YOUR_MEETUP_LOGIN_NAME_HERE)
    
    #Do the same thing for password and fill in.
    sb = browser.find_element_by_name('password')
    sb.send_keys(YOUR_MEETUP_PASSWORD_HERE)
    sb.send_keys(Keys.RETURN)
    
    urla = YOUR_MEETUP_GROUP_URL_HERE
    
    actions = ActionChains(browser)
    actions.move_to_element('Membres')
    browser.find_element_by_xpath('//a[@href="%s"]' %(urla)).click()    
    
    s2 = gsfh(browser).find_all('li', {'class':'nav-pageitem'})
    
    pu = []
    
    for i in s2 :
        a = i.find_all('a')[0].get('href')
        b = i.find_all('a')[0].text
        
        if b == u'→'  or b == u'←' :
            pass
        elif b == u'10' :
    
            pu.append(a)
            action(browser=browser, a=a, b=b)
            get_mm(YOUR_MEETUP_GROUP_URL_HERE, YOUR_DIRECTORY_TO_SAVE_DATA, \
                    browser, t=5)
            html1 = browser.page_source
            #parse the html page with bs4.
            soup2 = bs(html1,'html.parser')
            s3 = soup2.find_all('li', {'class':'nav-pageitem'})
            for i in s3 :
                a1 = i.find_all('a')[0].get('href')
                b1 = i.find_all('a')[0].text 
                
                if a1 not in pu :
                    pu.append(a1)                
                    action(browser=browser, a=a1, b=b1)
                    get_mm(YOUR_MEETUP_GROUP_URL_HERE, \
                            YOUR_DIRECTORY_TO_SAVE_DATA, browser, t=5)
                else :
                    pass
                
                if b1 == u'→'  or b == u'←' :
                    pass
                elif b1 == u'14' :
    
                    if a1 not in pu :
                        pu.append(a1)                    
                        action(browser=browser, a=a1, b=b1)
                        get_mm(YOUR_MEETUP_GROUP_URL_HERE, \
                                YOUR_DIRECTORY_TO_SAVE_DATA, browser, t=5)
                    else :
                        pass
                    
                    html2 = browser.page_source
                    soup3 = bs(html2,'html.parser')
                    s4 = soup3.find_all('li', {'class':'nav-pageitem'})
                    for i in s4 :
                        a2 = i.find_all('a')[0].get('href')
                        b2 = i.find_all('a')[0].text 
                        
                        if a2 not in pu :
                            pu.append(a2)                        
                            action(browser=browser, a=a2, b=b2)
                            get_mm(YOUR_MEETUP_GROUP_URL_HERE, \
                                    YOUR_DIRECTORY_TO_SAVE_DATA, browser, t=5)
                        else :
                            pass                     
        else : 
            pu.append(a)
            action(browser=browser, a=a, b=b)
            get_mm(YOUR_MEETUP_GROUP_URL_HERE, YOUR_DIRECTORY_TO_SAVE_DATA, \
                    browser, t=3)

#-----------------------------------------------------------------------------#

if __name__ == "__main__" :
    
    today_date = datetime.date.today().isoformat()
    #example of my login adress
    YOUR_MEETUP_LOGIN_GROUP_URL_HERE = "https://secure.meetup.com/fr-FR/login/?returnUri=https%3A%2F%2Fwww.meetup.com%2Ffr-FR%2Fcultiver-autrement-des-legumes-a-paris%2F"    
    YOUR_MEETUP_GROUP_URL_HERE = "your_meetup.com_group_url" + "/members/"
    YOUR_MEETUP_LOGIN_NAME_HERE = "your_meetup.com_login"
    YOUR_MEETUP_PASSWORD_HERE = 'your_password'
    YOUR_DIRECTORY_TO_SAVE_DATA = 'C:/__%s__/' %(today_date) 
    
    main(YOUR_DIRECTORY_TO_SAVE_DATA, YOUR_MEETUP_LOGIN_GROUP_URL_HERE, \
            YOUR_MEETUP_GROUP_URL_HERE, YOUR_MEETUP_LOGIN_NAME_HERE, \
            YOUR_MEETUP_PASSWORD_HERE)

    
