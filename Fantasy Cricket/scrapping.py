from bs4 import BeautifulSoup
import requests

file_name = input('Enter the file name : ')
innings = int(input('Enter the number of innings : '))
link = input('Enter the url of the scorecard : ')
html_text = requests.get(link).text

soup = BeautifulSoup(html_text,'lxml')
f = open(file_name+'.txt','w')

for i in range(1,innings+1):
        first_innings = soup.find('div',id='innings_'+str(i))
        scorecard = first_innings.find('div',class_ = 'cb-col cb-col-100 cb-ltst-wgt-hdr')

        rows = scorecard.find_all('div',class_ = 'cb-col cb-col-100 cb-scrd-itms')

        for row in rows:
            try:
                name = row.a.text.strip()
                f.write('{}\n'.format(name))

                wicket = row.find('span',class_ = 'text-gray').text.strip()
                f.write('{}\n'.format(wicket))

                runs = row.find('div',class_ = 'cb-col cb-col-8 text-right text-bold').text
                f.write('{}\n'.format(runs))

                balls = row.find('div',class_ = 'cb-col cb-col-8 text-right').text
                f.write('{}\n'.format(balls))
                f.write('{}\n'.format('Ignore'))
                f.write('{}\n'.format('Ignore'))
                f.write('{}\n'.format('Ignore'))
            except:
                break
f.close()

    
