# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------#

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as bs
import time
import os
import datetime
import json

#-----------------------------------------------------------------------------#

#text file connection. 
def txt_wd(YOUR_DIRECTORY_TO_SAVE_DATA, data) :
    
#    print type(data), data, '\n'
    
    rep_dir= YOUR_DIRECTORY_TO_SAVE_DATA
    book_name = '%s.txt' %(data['name'])
    
    if os.path.exists(rep_dir) :
        #encode data to json type.
        with open(rep_dir + book_name, 'w') as f :
            json.dump(data, f, sort_keys = True)            
    else : 
        print 'Directory', rep_dir, 'does not exists'
        print 'Create', rep_dir, 'directory', '\n'
        #create folder if not exist.
        os.mkdir(rep_dir)
        #encode data to json type.
        with open(rep_dir + book_name, 'w') as f :
            json.dump(data, f, sort_keys = True)            
    #close file.
    f.close()         
        
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

def get_mm_data(YOUR_DIRECTORY_TO_SAVE_DATA, browser, x, y, s='yes') :

#    print x, '\n'
#    print y, '\n'
    
    STATUS = s #STATUS (='no'(off),='yes'(on))   
    
    if STATUS == 'no' :
        pass
    elif STATUS == 'yes' :
        
        dict1 = {}
        
        #get meetup member name and profile page url.
        g = gsfh(browser).find_all('span', {'itemprop' : 'name'})[0].text
        #get data from get_mm function.
        dict1['today_date'] = x
        dict1['last_con'] = y
        dict1['name'] = g.lower()
        dict1['profile_url'] = browser.current_url

        #get meetup members location.     
        a = gsfh(browser).find_all('span', {'class' : 'locality'})
        location = a[1].text#.strip()
        dict1['location'] = location
    
        #get meetup members membership date.
        b = gsfh(browser).find_all('div', {'class' : 'unit size1of3'})  
        gm_date = b[1].find_all('p')[0].text
        gm_date = gm_date.split(' ')
        #calcul des mois.
        if gm_date[1] == u'd\xe9cembre' :
            mois_num = u'12'
        elif gm_date[1] == u'novembre' :           
            mois_num = u'11'
        elif gm_date[1] == u'octobre' :
            mois_num = u'10'
        elif gm_date[1] == u'septembre' :
            mois_num = u'09'            
        elif gm_date[1] == u'ao\xfbt' :
            mois_num = u'08'
        elif gm_date[1] == u'juillet' :
            mois_num = u'07'
        elif gm_date[1] == u'juin' :
            mois_num = u'06'
        elif gm_date[1] == u'mai' :           
            mois_num = u'05'
        elif gm_date[1] == u'avril' :
            mois_num = u'04'
        elif gm_date[1] == u'mars' :
            mois_num = u'03'
        elif gm_date[1] == u'f\xe9vrier' :         
            mois_num = u'02'
        elif gm_date[1] == u'janvier' :            
            mois_num = u'01'
        else :
            pass
        
        if int(gm_date[0]) < 10 :
            gm_date = '0' + gm_date[0] +  '/' + mois_num + '/' + gm_date[2].replace('20','')
        else :
            gm_date = gm_date[0] +  '/' + mois_num + '/' + gm_date[2].replace('20','')
        dict1['gm_date'] = gm_date
        
        #get meetup members membership photo url.
        c = gsfh(browser).find_all('img', \
                    {'class' : 'D_memberProfilePhoto photo big-preview-photo'})
        thumb_url = c[0].get('src')
        dict1['thumb_url'] = thumb_url
        
        #get meetup members common membership group name.
        d = gsfh(browser).find_all('div', {'class' : 'figureset-description'})
        d1 = [i.find_all('a') for i in d] 
        cmgl, cmgd = [], {}
        for j in d1 :
            cmgd['%s' %(j[0].text)] = j[0].get('href')
            cmgl.append(j)
        dict1['common_group'] = cmgd
        dict1['common_group_num'] = len(cmgl)
        
        #get meetup members other groups (all groups).
        e = gsfh(browser).find_all('ul', {'id' : 'my-meetup-groups-list'})
        try : 
            e1 = [i.find_all('div', {'class' : 'D_name bold'}) for i in e][0]
            mogl, mogd = [], {}
            for k in e1 :
                k1 = k.find_all('a', {'class' : 'omnCamp omngj_pcg4'})[0]        
                mogd['%s' %(k1.text)] = k1.get('href')
                mogl.append(k)
            dict1['other_group'] = mogd
            dict1['other_group_num'] = len(mogl)
        except : 
            mogl, mogd = [], {}            
            dict1['other_group'] = mogl
            dict1['other_group_num'] = len(mogl)
            
        #get meetup member personnal interests.
        f = gsfh(browser).find_all('ul', {'id' : 'memberTopicList'})
        f1 = [i.find_all('a') for i in f][0]
        mpil, mpid = [], {}
        for l in f1 :
            mpid[l.text] = l.get('href')
            mpil.append(l)
        dict1['personnal_interests'] = mpid
        dict1['personnal_interests_num'] = len(mpil)
             
        #write data to excel file.
        txt_wd(YOUR_DIRECTORY_TO_SAVE_DATA, data=dict1)
        
        print dict1, '\n'
        
        return dict1

#-----------------------------------------------------------------------------#

def get_mm(YOUR_MEETUP_GROUP_URL_HERE, YOUR_DIRECTORY_TO_SAVE_DATA, \
            browser, t=3) :
    
    h = gsfh(browser).find_all('ul',{'id' : 'memberList'})[0]
    h = h.find_all('a', {'class' : 'memName'})

    #data to pass to get_mm_data in data disctionnary.
    l1 = []
    for i in h :
#        a = i.find_all('span')#[0]#.text.strip()
        a = datetime.date.today()
        a = a.strftime("%d/%m/%y")
        l1.append(a)

    #get meetup member last visit to meetup page.
    p = gsfh(browser).find_all('ul', \
                {'class' : 'resetList clear-both memberStats small'})
    
    #data to pass to get_mm_data in data disctionnary.            
    l2 = []
    for i in p :
        a = i.find_all('span')[1].text.strip()
        l2.append(a)

    mytext = YOUR_MEETUP_GROUP_URL_HERE
    item_list = []
    
    for i in h : 
        d = {}
        x = i.get('href').replace(mytext,'').replace('/','').strip()
        y = i.text
        d['%s' %(x)]  = y
        item_list.append(d)

    #moving on web pages.
    num2 = -1
    for j in item_list :
        num2 += 1
        memnum = j.keys()[0]
        elem = j[memnum]
        link = YOUR_MEETUP_GROUP_URL_HERE + "%s/" %(memnum)
        actions = ActionChains(browser)
        actions.move_to_element('%s' %(elem)) 
        browser.find_element_by_xpath('//a[@href="%s"]' %(link)).click()
        #use of gmm_data here to get members data like in the meetup API
        #get meetup members data and write it to :
        #excel file
        get_mm_data(YOUR_DIRECTORY_TO_SAVE_DATA, browser, x= l1[num2], y=l2[num2])
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
    YOUR_MEETUP_LOGIN_GROUP_URL_HERE = "https://secure.meetup.com/fr-FR/login/?returnUri=https%3A%2F%2Fwww.meetup.com%2Ffr-FR%2Fcultiver-autrement-des-legumes-a-paris%2F"    
    YOUR_MEETUP_GROUP_URL_HERE = "your_meetup.com_group_url" + "/members/"
    YOUR_MEETUP_LOGIN_NAME_HERE = "your_meetup.com_login"
    YOUR_MEETUP_PASSWORD_HERE = 'your_password'
    YOUR_DIRECTORY_TO_SAVE_DATA = 'C:/__%s__/' %(today_date) 
    
    main(YOUR_DIRECTORY_TO_SAVE_DATA, YOUR_MEETUP_LOGIN_GROUP_URL_HERE, \
            YOUR_MEETUP_GROUP_URL_HERE, YOUR_MEETUP_LOGIN_NAME_HERE, \
            YOUR_MEETUP_PASSWORD_HERE)

    
