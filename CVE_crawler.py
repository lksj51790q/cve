import requests
from dateutil.parser import parse
import bs4, time, random

"""
從各年分爬第一個結果
例如 : http://www.cvedetails.com/vulnerability-list/year-2014/vulnerabilities.html
將會是 CVE-2014-9433 為最大ID
接著往前遍歷即可(中間依舊可能有不存在之ID)
遍歷 : CVE-2014-9433 ~ CVE-2014-0001 (ID至少4位數)

頁面
例如 : http://www.cvedetails.com/cve/CVE-2004-0903/

特殊:
http://www.cvedetails.com/cve/CVE-2007-5421/
"""


class CVECrawler(object):

	def __init__(self):

		self.cve_id = None			#str
		self.cvss_score = None		#float
		self.conf = None			#str
		self.integ = None			#str
		self.avail = None			#str
		self.gain_access = None		#str
		self.complexity = None		#str
		self.authentication = None	#str
		self.cwe_id = None			#int
		self.publish_date = None	#datetime
		self.update_date = None		#datetime
		self.description = None		#str
		self.pruduct = []			#str list
		self.vendor = []			#str list
		self.product_type = []		#str list
		self.version = []			#str list
		self.update_ = []			#str list
		self.edition = []			#str list
		self.language = []			#str list

	def clear(self):
		#clear all class variables
		self.cve_id = None			#str
		self.cvss_score = None		#float
		self.conf = None			#str
		self.integ = None			#str
		self.avail = None			#str
		self.gain_access = None		#str
		self.complexity = None		#str
		self.authentication = None	#str
		self.cwe_id = None			#int
		self.publish_date = None	#datetime
		self.update_date = None		#datetime
		self.description = None		#str
		self.pruduct = []			#str list
		self.vendor = []			#str list
		self.product_type = []		#str list
		self.version = []			#str list
		self.update_ = []			#str list
		self.edition = []			#str list
		self.language = []			#str list
		return

	def get_cve_info(self):
		return [self.cve_id, 
		self.cvss_score, 
		self.conf, 
		self.integ, 
		self.avail, 
		self.gain_access, 
		self.complexity, 
		self.authentication, 
		self.cwe_id, 
		self.publish_date, 
		self.update_date, 
		self.description
		]

	def get_cve_pruduct_info(self):
		return [self.cve_id, 
		self.product_type,
		self.vendor,
		self.pruduct,
		self.version, 
		self.update_, 
		self.edition, 
		self.language
		]

	def get_cve_id_by_year(self, year):

		if int(year) < 1999:
			return 0
		url = 'http://www.cvedetails.com/vulnerability-list/year-' + str(year) + '/vulnerabilities.html'
		cve = requests.Session()
		headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36", "referer":'http://www.cvedetails.com/'}
		
		for i in range(0,10):
			try:
				target = cve.get(url, headers=headers, timeout=5)
			except:
				time.sleep(random.randint(5,20))
				continue
			break

		if (target.status_code != requests.codes.ok):
			raise RequestError('\n' + target.url+'\ncve list request failed, status '+str(target.status_code)+'\nPlease check your internet.')
			return -1

		soup = bs4.BeautifulSoup(target.text, "lxml")
		last_page = int(soup.find('div', class_="paging", id="pagingb").findAll('a')[-1].text)
		data_num = int(soup.find('div', class_="paging", id="pagingb").find('b').text)

		#return page_num and datanum
		yield [data_num, last_page]

		#first page
		for ele in soup.findAll('tr', class_="srrowns"):
			yield [int(ele.findAll("td")[1].a.get("href").split("/")[-2].split("-")[-2]), int(ele.findAll("td")[1].a.get("href").split("/")[-2].split("-")[-1])]

		#other page
		for page in range(2,last_page+1): 
			url = 'http://www.cvedetails.com/' + soup.find('a', title="Go to page "+str(page)).get('href')
			for i in range(0,10):
				try:
					target = cve.get(url, headers=headers, timeout=5)
				except:
					time.sleep(random.randint(5,20))
					continue
				break

			if (target.status_code != requests.codes.ok):
				raise RequestError('\n' + target.url+'\ncve list request failed, status '+str(target.status_code)+'\nPlease check your internet.')
				return -1

			soup = bs4.BeautifulSoup(target.text, "lxml")
			for ele in soup.findAll('tr', class_="srrowns"):
				yield [int(ele.findAll("td")[1].a.get("href").split("/")[-2].split("-")[-2]), int(ele.findAll("td")[1].a.get("href").split("/")[-2].split("-")[-1])]
			
		return

	def set_target_cve(self, cve_id):

		self.cve_id = cve_id
		url = 'http://www.cvedetails.com/cve/' + cve_id + '/'
		cve = requests.Session()
		headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36", "referer":'http://www.cvedetails.com/'}
		
		for i in range(0,10):
			try:
				target = cve.get(url, headers=headers, timeout=0.5)
			except:
				time.sleep(random.randint(5,20))
				continue
			break

		if (target.status_code != requests.codes.ok):
			raise RequestError('\n' + target.url+'\ncve list request failed, status '+str(target.status_code)+'\nPlease check your internet.')
			self.clear()
			return False
		soup = bs4.BeautifulSoup(target.text, "lxml")

		if not soup.findAll("span",class_="cvssdesc"):
			self.clear()
			return False
		for trash in soup.findAll("span",class_="cvssdesc"):
			trash.extract()
		try:
			element = soup.find('table', id="cvssscorestable", class_="details").findAll("td")
			self.cvss_score = float(element[0].text.strip())
			self.conf = element[1].text.strip()
			self.integ = element[2].text.strip()
			self.avail = element[3].text.strip()
			self.gain_access = element[6].text.strip()
			self.complexity = element[4].text.strip()
			self.authentication = element[5].text.strip()
		except:
			self.clear()
			return False
		try:
			self.cwe_id = int(element[-1].text.strip())
		except:
			self.cwe_id = None

		element =  soup.find('span', class_="datenote")
		element.extract()
		element =  element.string.strip().split()
		self.publish_date = parse(element[3])
		self.update_date = parse(element[-1])

		element = soup.find('div', class_="cvedetailssummary")
		self.description = element.text.strip().replace("\\","\\\\").replace("'","\\'")

		table = soup.find('table', class_="listtable")
		while table != None:
			ths = table.findAll("th")
			for i in range(0,len(ths)):
				ths[i] = ths[i].text
			if ths == ['#', 'Product Type', 'Vendor', 'Product', 'Version', 'Update', 'Edition', 'Language', '']:
				for ele in table.findAll("tr")[1:]:
					element = ele.findAll("td")
					self.pruduct.append(element[3].text.strip())
					self.vendor.append(element[2].text.strip())
					self.product_type.append(element[1].text.strip())
					if element[4].text.strip():
						self.version.append(element[4].text.strip())
					else:
						self.version.append(None)
					if element[5].text.strip():
						self.update_.append(element[5].text.strip())
					else:
						self.update_.append(None)
					if element[6].text.strip():
						self.edition.append(element[6].text.strip())
					else:
						self.edition.append(None)
					if element[7].text.strip():
						self.language.append(element[7].text.strip())
					else:
						self.language.append(None)

				break

			table.extract()
			table = soup.find('table', class_="listtable")

		return True

	

class EDBCrawler(object):

	def init(self):

		self.title = None			#str
		self.edb_id = None			#int
		self.author = None			#str
		self.publish = None			#datetime
		self.cve_id = None			#str
		self.type = None			#str
		self.platform = None		#str
		self.code = None			#str

	def clear(self):

		self.title = None			#str
		self.edb_id = None			#int
		self.author = None			#str
		self.publish = None			#datetime
		self.cve_id = None			#str
		self.type = None			#str
		self.platform = None		#str
		self.code = None			#str
		return

	def get_edb_info(self):
		return[self.edb_id,
		self.title,
		self.author,
		self.publish,
		self.cve_id,
		self.type,
		self.platform,
		self.code
		]

	def get_edb_id_by_page(self, page):

		url = 'https://www.exploit-db.com/browse/'
		edb = requests.Session()
		headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36", "referer":'https://www.exploit-db.com/'}
		payload = {'order':'desc', 'pg':str(page)}

		for i in range(0,10):
			try:
				target = edb.get(url, headers=headers, params=payload, timeout=5)
			except:
				time.sleep(random.randint(20,60))
				continue
			break
			
		if (target.status_code != requests.codes.ok):
			raise RequestError('\n' + target.url+'\ncve list request failed, status '+str(target.status_code)+'\nPlease check your internet.')
			return

		soup = bs4.BeautifulSoup(target.text, "lxml")
		for i in soup.findAll('td',class_="description"):
			if i.a.get("href").split("/")[-3] == "exploits":
				yield (i.a.get("href").split("/")[-2])
		return

	def set_target_edb(self, edb_id):

		self.edb_id = int(edb_id)
		url = 'https://www.exploit-db.com/exploits/' + str(self.edb_id) + '/'
		edb = requests.Session()
		headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36", "referer":'https://www.exploit-db.com/'}
		
		for i in range(0,10):
			try:
				target = edb.get(url, headers=headers, timeout=5)
			except:
				time.sleep(random.randint(20,60))
				continue
			break

		if (target.status_code != requests.codes.ok):
			raise RequestError('\n' + target.url+'\ncve list request failed, status '+str(target.status_code)+'\nPlease check your internet.')
			return False

		result = []
		soup = bs4.BeautifulSoup(target.text, "lxml")
		self.title = soup.find('h1').text.strip().replace("\\","\\\\").replace("'","\\'")

		for i in soup.find('table', class_="exploit_list").findAll("td")[1:6]:
			if i.text.strip().split()[1] == "N/A":
				result.append(None)
			else:
				result.append(i.text.strip().split(maxsplit=1)[1])

		self.author = result[0].replace("\\","\\\\").replace("'","\\'")
		self.publish = parse(result[1])
		self.cve_id = result[2]
		self.type = result[3].replace("\\","\\\\").replace("'","\\'")
		self.platform = result[4].replace("\\","\\\\").replace("'","\\'")

		time.sleep(random.randint(5,20))
		url = 'https://www.exploit-db.com/raw/' + str(edb_id) + '/'
		for i in range(0,10):
			try:
				target = edb.get(url, headers=headers, timeout=5)
			except:
				time.sleep(random.randint(20,60))
				continue
			break

		if (target.status_code != requests.codes.ok):
			raise RequestError('\n' + target.url+'\ncve list request failed, status '+str(target.status_code)+'\nPlease check your internet.')
			return False
		self.code = target.text.replace("\\","\\\\").replace("'","\\'")

		return True
