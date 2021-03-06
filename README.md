須先行安裝模組：<br>
&emsp;CVE_crawler.py : requests, bs4, dateutil<br>
&emsp;CVE_spider.py : pymysql<br>

CVE_crawler.py:<br>
&emsp;包含兩物件：<br>
&emsp;&emsp;CVECrawler 及 EDBCrawler<br><br>
&emsp;&emsp;CVECrawler 使用方式：<br>
&emsp;&emsp;&emsp;get_cve_id_by_year(year)<br>
&emsp;&emsp;&emsp;&emsp;回傳 list[year, id]的generator<br><br>
&emsp;&emsp;&emsp;set_target_cve(cve_id)<br>
&emsp;&emsp;&emsp;&emsp;目標內容抓取成功回傳true, 否則false<br><br>
&emsp;&emsp;&emsp;clear()<br>
&emsp;&emsp;&emsp;&emsp;清除物件先前內容, 每次呼叫set_target_cve()都應清除一次<br><br>
&emsp;&emsp;&emsp;get_cve_info()<br>
&emsp;&emsp;&emsp;&emsp;回傳 list [(string)cve id, <br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(float)cvss score, <br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(string)confidentiality, <br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(string)integrity, <br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(string)availability, <br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(string)gain access, <br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(string)access complexity, <br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(string)authentication, <br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(int)cwe_id, <br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(datetime)publish date, <br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(datetime)update date,<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(string)description<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;]<br><br>
&emsp;&emsp;&emsp;get_cve_pruduct_info()<br>
&emsp;&emsp;&emsp;&emsp;回傳 list [(string)cve id,<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(string)[product type list],<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(string)[vendor list],<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(string)[pruduct list],<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(string)[version list],<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(string)[update list],<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(string)[edition list],<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(string)[language list]<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;]<br><br>
&emsp;&emsp;EDBCrawler 使用方式：<br>
&emsp;&emsp;&emsp;get_edb_id_by_page(page)<br>
&emsp;&emsp;&emsp;&emsp;回傳 edb id 的 generator<br><br>
&emsp;&emsp;&emsp;set_target_edb(edb id)<br>
&emsp;&emsp;&emsp;&emsp;目標內容抓取成功回傳true, 否則false<br><br>
&emsp;&emsp;&emsp;clear()<br>
&emsp;&emsp;&emsp;&emsp;清除物件先前內容, 每次呼叫set_target_edb()都應清除一次<br><br>
&emsp;&emsp;&emsp;get_edb_info()<br>
&emsp;&emsp;&emsp;&emsp;回傳 list [(int)edb id, <br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(string)title,<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(string)author,<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(datetime)publish,<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(string)cve id,<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(string)type,<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(string)platform,<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(string)code<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;]<br>

CVE_spider.py:<br>
Usage:<br>
&emsp;CVE_spider <instruction> [option]<br><br>
Instructions:<br><br>
&emsp;database:<br>
&emsp;&emsp;set database's configuration<br>
&emsp;&emsp;Options:<br>
&emsp;&emsp;&emsp;-c, --connect<br>
&emsp;&emsp;&emsp;&emsp;connect to target database and store the link informations<br>
&emsp;&emsp;&emsp;-s, --construct<br>
&emsp;&emsp;&emsp;&emsp;create table to specified database<br><br>
&emsp;help:<br>
&emsp;&emsp;print this help message<br><br>
&emsp;scrapy:<br>
&emsp;&emsp;scrapy target website<br>
&emsp;&emsp;Options:<br>
&emsp;&emsp;&emsp;-c, --cve [target year]<br>
&emsp;&emsp;&emsp;&emsp;scrapy cve from target year list, year range from 1999<br>
&emsp;&emsp;&emsp;-e, --edb [target page]<br>
&emsp;&emsp;&emsp;&emsp;scrapy exploit database from target page, specific range is necessary ex.page one to five : 1-5<br>
      
