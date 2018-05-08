# -*- coding: utf-8 -*-
import requests
from lxml import etree
import json
# from selenium import webdriver

base_link = 'http://sgnweb.nccu.edu.tw'
employee_base_link = 'http://sgnweb.nccu.edu.tw/AddressBook/AddressBook/StaffDetail?id=%s'

datas = dict()
# browser = webdriver.PhantomJS(executable_path="/Users/blockchain/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs")

KEYLIST = [
	'name', 'title', 'ext', 'email', 'job', 'master'
]

def main () :

	for url in getUrls() :

		if url == '#' :
			continue

		else :
			link = base_link + url
			print (link)

			# browser.get( 'http://sgnweb.nccu.edu.tw/AddressBook/AddressBook/ListStaff?utCod=H01' )
			# res = browser.page_source

			res = requests.get( link ).text
			source = etree.HTML(res)

			names, job = getNameAndJob( source )
			infos = getInfoPage( source )

			assert len(names) == len(infos)

 
			for i in range( len(names) ) :
				infos[i].append('JOBS：%s' % (job))
				datas[names[i]] = infos[i]


			# print( datas )
			# break			

#

	writeDatas( datas )


def getNameAndJob( source ):
	names = list()
	infos = source.xpath('//div[@class="panel-heading"]/text()')
	job = source.xpath('//h4//text()')[0]

	for info in infos :
		names.append( "".join( info.split() ) )

	# print( names )

	return names, job

def getInfoPage( source ) :

	infos = []

	employeeID = source.xpath('//div[@class="panel panel-default"]/@id')
	try :
		for ID in employeeID :
			employee_link = employee_base_link % (ID)

			info = requests.get( employee_link ).text
			infoSrc = etree.HTML(info)
			total = " ".join( str(infoSrc.xpath('string(//body)')).split() )

			infos.append( total.split(' ') )

	except Exception as e :
		print( str(e) )

	return infos


def getUrls() :

	res = requests.get( base_link + '/AddressBook/' ).text
	source = etree.HTML(res)
	return source.xpath('//li/a/@href')

def writeDatas( datas ) :
	with open ( 'teacher.json', 'w', encoding='utf-8' ) as outfile :
		
		infos = list()
		for name in datas.keys() :
			personalInfo = dict()
			personalInfo['name'] = name
			for data in datas[name] :
				cont = data.split('：')
				key = ''
				if cont[0] == '職稱':
					key = 'title'
				if cont[0] == '分機':
					key = 'ext'
				if cont[0] == '電子郵件':
					key = 'email'
				if cont[0] == 'JOBS':
					key = 'job'
				if cont[0] == '個人學術專長':
					key = 'master'
				
				try:
					personalInfo[key] = cont[1]
				except:
					personalInfo[key] = ""

			for left in list( set(KEYLIST) - set(personalInfo.keys() ) ) :
				personalInfo[left] = ""

			infos.append( personalInfo )

		json.dump( infos, outfile, sort_keys=True, indent=4, ensure_ascii=False)
		outfile.close()

def temp() :
	with open( 'temp.json', 'r', encoding='utf-8' ) as f :
		data = f.read()
		print( list('[1,2,3]'))
		print( type(data))


if __name__ == '__main__':
	main()
	# temp()