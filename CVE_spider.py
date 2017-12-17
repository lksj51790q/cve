#!/usr/bin/python3
#CVE_spider
import sys

def usage():
	print('\033[33m'+"""
Usage:
  CVE_spider <instruction> [option]

Instructions:

  database:
    set database's configuration
    Options:
      -c, --connect    connect to target database and store the link informations
      -s, --construct  create table to specified database

  help
    print this help message

  scrapy
    scrapy target website
    Options:
      -c, --cve [target year]  scrapy cve from target year list, year range from 1999
      -e, --edb [target page]  scrapy exploit database from target page, specific range is necessary ex.page one to five : 1-5
		"""+'\033[0m')


def version():
	print('\033[33m'+"1.0"+'\033[0m')


if __name__ == '__main__':

	#If there exist no command
	if not len(sys.argv[1:]):
		usage()
		sys.exit(0)

	#Parse command and options
	if sys.argv[1] in ["help", "--help", "-h"]:
		usage()
		sys.exit(0)

	#Parse command and options
	if sys.argv[1] in ["version", "--version", "-v"]:
		version()
		sys.exit(0)

	#check at least one instruction exist
	if sys.argv[1] not in ["scrapy", "database"]:
		print("Invalid instruction \"" + sys.argv[1] + "\"")
		print("Try 'CVE_spider help' for more information")
		sys.exit(1)

	#check at least one instruction's option exist
	if len(sys.argv[1:]) == 1:
		print("Instruction \"" + sys.argv[1] + "\" must be at least one option")
		print("Try 'CVE_spider help' for more information")
		sys.exit(1)

	import getopt, os, pickle

	#check configure file, if not exist then create one
	###use os.path.realpath() can get this program's absolute path even excute from linux soft link
	config = "/".join(os.path.realpath(__file__).split("/")[:-1]) + "/cve.conf"
	try:
		open(config).close()
	except:
		conf = open(config, "wb")
		pickle.dump({'database':{}}, conf, 1)
		conf.close()

	if sys.argv[1] == "database":

		try:
			opts,args = getopt.getopt(sys.argv[2:], "cs", ["connect", "construct"])
		except getopt.GetoptError as e:
			print("Invalid option \"" + e.opt + "\"")
			print("Try 'CVE_spider help' for more information")
			sys.exit(1)

		if len(args):
			print("Invalid argument \"" + "\", \"".join(args) + "\"")
			print("There should be no argument for instruction \"" + sys.argv[1] + "\"")
			print("Try 'CVE_spider help' for more information")
			sys.exit(1)

		for opt, arg in opts:
			if opt in ["-c","--connect"]:
				try:
					conf = open(config, "rb")
					conf_dict = pickle.load(conf)
					conf.close()
				except:
					print('\033[31mDatabase configure file read failed\033[0m')
					sys.exit(1)

				configure_chk = False
				if "host" not in conf_dict["database"].keys():
					configure_chk = True
				elif "user" not in conf_dict["database"].keys():
					configure_chk = True
				elif "password" not in conf_dict["database"].keys():
					configure_chk = True

				if not configure_chk:
					answer = input("There already exist database configure, do you want to update it? (y/n)")
					if answer not in ["Y","y","N","n"]:
						print("Invalid input")
						sys.exit(1)
					elif answer in ["Y","y"]:
						pass
					elif answer in ["N","n"]:
						sys.exit(1)
					else:
						assert False,answer

				import getpass
				host = input("Host : ")
				user = input("User : ")
				password = getpass.getpass(prompt="Password : ")
				while password != getpass.getpass(prompt="Password confirm : "):
					print("Passwords are not consistent")
					password = getpass.getpass(prompt="Password : ")
				import pymysql
				try:
					pymysql.connect(host = host, port = 3306, user = user, password = password, charset = 'utf8').close()
				except pymysql.Error:
					print('\033[31mDatabase connect failed\033[0m')
					sys.exit(1)
				try:
					conf_dict["database"].update({'host':host, 'user':user, 'password':password})
					conf = open(config, "wb")
					pickle.dump(conf_dict, conf, 1)
					conf.close()
					print('\033[33mDatabase configure update successfully\033[0m')
				except:
					print('\033[31mDatabase configure update failed\033[0m')
					sys.exit(1)

			elif opt in ["-s","--construct"]:
				
				try:
					conf = open(config, "rb")
					conf_dict = pickle.load(conf)
					conf.close()
				except:
					print('\033[31mDatabase configure load failed\033[0m')
					sys.exit(1)

				import pymysql

				try:
					db = pymysql.connect(host = conf_dict["database"]["host"], port = 3306, user = conf_dict["database"]["user"], password = conf_dict["database"]["password"], charset = 'utf8')
				except pymysql.Error:
					print('\033[31mDatabase connect failed\033[0m')
					sys.exit(1)
				except KeyError:
					print('\033[31mThere is no connectable database\033[0m')
					print("Try 'CVE_spider database -c' to connect a database")
					sys.exit(1)

				try:
					print("Database name : ",conf_dict["database"]["db"])
					answer = input("Do you want to change? (y/n)")
					if answer not in ["Y","y","N","n"]:
						print("Invalid input")
						sys.exit(1)
					elif answer in ["Y","y"]:
						db_name = input("Database name : ")
					elif answer in ["N","n"]:
						db_name = conf_dict["database"]["db"]
					else:
						assert False,answer
				except KeyError:
					db_name = input("Database name : ")

				sql = """
				SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
				SET time_zone = "+00:00";

				/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
				/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
				/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
				/*!40101 SET NAMES utf8mb4 */;

				CREATE DATABASE IF NOT EXISTS `""" + db_name + """` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci;
				USE `""" + db_name + """`;

				CREATE TABLE `cve_info` (
				  `CVE_ID` varchar(20) COLLATE utf8mb4_unicode_520_ci NOT NULL,
				  `CVSS_score` decimal(3,1) UNSIGNED NOT NULL COMMENT '0.0-10.0',
				  `conf` tinyint(1) DEFAULT NULL COMMENT '0=none, 1=partial, 2=complete',
				  `integ` tinyint(1) DEFAULT NULL COMMENT '0=none, 1=partial, 2=complete',
				  `avail` tinyint(1) DEFAULT NULL COMMENT '0=none, 1=partial, 2=complete',
				  `gain_access` tinyint(1) NOT NULL COMMENT '0=none, 1=admin',
				  `complexity` tinyint(1) DEFAULT NULL COMMENT '0=low, 1=medium, 2=high',
				  `authentication` tinyint(1) DEFAULT NULL COMMENT '0=none, 1=single, 2=mutiple',
				  `CWE_ID` smallint(1) UNSIGNED DEFAULT NULL,
				  `publish_date` date NOT NULL,
				  `update_date` date NOT NULL,
				  `description` text COLLATE utf8mb4_unicode_520_ci NOT NULL
				) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

				CREATE TABLE `exploit` (
				  `EDB_ID` int(1) NOT NULL,
				  `title` varchar(200) COLLATE utf8mb4_unicode_520_ci NOT NULL,
				  `author` varchar(50) COLLATE utf8mb4_unicode_520_ci NOT NULL,
				  `publish` date NOT NULL,
				  `CVE_ID` varchar(20) COLLATE utf8mb4_unicode_520_ci NOT NULL,
				  `type` varchar(20) COLLATE utf8mb4_unicode_520_ci NOT NULL,
				  `platform` varchar(20) COLLATE utf8mb4_unicode_520_ci NOT NULL,
				  `code` text COLLATE utf8mb4_unicode_520_ci NOT NULL
				) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

				CREATE TABLE `pruducts` (
				  `CVE_ID` varchar(20) COLLATE utf8mb4_unicode_520_ci NOT NULL,
				  `pruduct_type` varchar(20) COLLATE utf8mb4_unicode_520_ci NOT NULL,
				  `vendor` varchar(100) COLLATE utf8mb4_unicode_520_ci NOT NULL,
				  `pruduct` varchar(100) COLLATE utf8mb4_unicode_520_ci NOT NULL,
				  `version` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
				  `update_` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
				  `edition` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
				  `language` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL
				) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;


				ALTER TABLE `cve_info`
				  ADD PRIMARY KEY (`CVE_ID`);

				ALTER TABLE `exploit`
				  ADD PRIMARY KEY (`EDB_ID`),
				  ADD KEY `EDB_ID` (`EDB_ID`),
				  ADD KEY `CVE_ID` (`CVE_ID`),
				  ADD KEY `author` (`author`),
				  ADD KEY `publish` (`publish`),
				  ADD KEY `type` (`type`),
				  ADD KEY `platform` (`platform`);

				ALTER TABLE `pruducts`
				  ADD KEY `CVE_ID` (`CVE_ID`),
				  ADD KEY `pruduct` (`pruduct`),
				  ADD KEY `vendor` (`vendor`),
				  ADD KEY `pruduct_type` (`pruduct_type`);


				ALTER TABLE `pruducts`
				  ADD CONSTRAINT `pruducts_ibfk_1` FOREIGN KEY (`CVE_ID`) REFERENCES `cve_info` (`CVE_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

				/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
				/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
				/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
				"""

				try:
					cursor = db.cursor()
					cursor.execute(sql)
					cursor.close()
					db.close()
					print('\033[33mDatabase construct successfully\033[0m')
					conf_dict["database"].update({'db':db_name})
					conf = open(config, "wb")
					pickle.dump(conf_dict, conf, 1)
					conf.close()
					print('\033[33mDatabase configure update successfully\033[0m')
				except :
					print('\033[31mDatabase construct failed\033[0m')
					sys.exit(1)

			else:
				assert False,opt


	elif sys.argv[1] == "scrapy":
		
		try:
			opts,args = getopt.getopt(sys.argv[2:], "c:e:", ["cve", "edb"])
		except getopt.GetoptError as e:
			if e.opt in ["c", "e", "cve", "edb"]:
				print("There should be an argument for option \"" + e.opt + "\"")
			print("Invalid option \"" + e.opt + "\"")
			print("Try 'CVE_spider help' for more information")
			sys.exit(1)

		if len(args):
			print("Invalid argument \"" + "\", \"".join(args) + "\"")
			print("There should be no argument for instruction \"" + sys.argv[1] + "\"")
			print("Try 'CVE_spider help' for more information")
			sys.exit(1)

		for opt, arg in opts:
			if opt in ["-c","--cve"]:

				import datetime
				print("parsing options...")
				try:
					year = int(arg)
					if year < 1999 or year > datetime.date.today().year:
						print("Invalid year ",arg)
						print("Year must be 1999-",datetime.date.today().year)
						sys.exit(1)
				except:
					print("Invalid year ",arg)
					print("Year must be 1999-",datetime.date.today().year)
					sys.exit(1)

				import pymysql
				print("loading database configure...")
				try:
					conf = open(config, "rb")
					conf_dict = pickle.load(conf)
					conf.close()
				except:
					print('\033[31mDatabase configure load failed\033[0m')
					sys.exit(1)
				print("connecting to database...")
				try:
					db = pymysql.connect(host = conf_dict["database"]["host"], port = 3306, user = conf_dict["database"]["user"], password = conf_dict["database"]["password"], db = conf_dict["database"]["db"], charset = 'utf8')
					cursor = db.cursor()
				except pymysql.Error:
					print('\033[31mDatabase connect failed\033[0m')
					sys.exit(1)
				except KeyError:
					print('\033[31mThere is no connectable database\033[0m')
					print("Try 'CVE_spider database -c' to connect a database")
					sys.exit(1)

				from CVE_crawler import CVECrawler
				import time, random, math
				print("initializing cve_spider...")
				cve = CVECrawler()
				store_num_dict = {'None':0, 'Not required':0, 'Low':0, 'Partial':1, 'Admin':1, 'Single system':1, 'Medium':1, 'User':2, 'Complete':2, 'High':2, 'Multiple system':2, 'Other':3}
				
				id_generator = cve.get_cve_id_by_year(year)
				[data_num, last_page] = next(id_generator)
				print("scrapy...")
				count = -1
				for i in id_generator:
					try:
						count += 1

						#transfer to ID
						ID = str(i[1])
						while len(ID) < 4:
							ID = "0" + ID
						ID = "cve-" + str(i[0]) + "-" + ID

						#print bar
						print(" [", end='')
						bar = ""
						for j in range(0, math.floor(count/data_num*50)):
							bar += "#"
						print(bar, end='')
						bar = ""
						for j in range(0, 50-math.floor(count/data_num*50)):
							bar += " "
						print(bar, end='')
						print("]", end='')
						print("%.02f%1s"% (count/data_num*100,"%"), end='')
						print("  "+ID+"      ", end='\r')

						#check database
						sql = "SELECT `CVE_ID` FROM `cve_info` WHERE `CVE_ID`='" + ID + "' LIMIT 1;"
						if cursor.execute(sql) != 0:
							cve.clear()
							continue
						if not cve.set_target_cve(ID):
							cve.clear()
							continue

						sql = "INSERT INTO `cve_info` (`CVE_ID`, `CVSS_score`, `conf`, `integ`, `avail`, `gain_access`, `complexity`, `authentication`, `CWE_ID`, `publish_date`, `update_date`, `description`) VALUES ('"
						result = cve.get_cve_info()
						sql += result[0] + "'," + str(result[1]) + ","
						for ele in result[2:8]:
							sql += str(store_num_dict[ele]) + ","
						if result[8] == None:
							sql += "NULL,'"
						else:
							sql += str(result[8]) + ",'"
						sql += str(result[9].date()) + "','" + str(result[10].date()) + "','" + result[11] + "');"
						cursor.execute(sql)

						result = cve.get_cve_pruduct_info()
						sql = "INSERT INTO `pruducts` (`CVE_ID`, `pruduct_type`, `vendor`, `pruduct`, `version`, `update_`, `edition`, `language`) VALUES"
						for i in range(0, len(result[1])):
							sql += "('" + result[0] + "','"
							sql += result[1][i] + "','"
							sql += result[2][i] + "','"
							sql += result[3][i] + "',"
							if result[4][i] is None:
								sql += "NULL,"
							else:
								sql += "'" + result[4][i] + "',"
							if result[5][i] is None:
								sql += "NULL,"
							else:
								sql += "'" + result[5][i] + "',"
							if result[6][i] is None:
								sql += "NULL,"
							else:
								sql += "'" + result[6][i] + "',"
							if result[7][i] is None:
								sql += "NULL),"
							else:
								sql += "'" + result[7][i] + "'),"
						sql = sql[:-1] + ";"
						cursor.execute(sql)

						db.commit()
						cve.clear()

						time.sleep(random.randint(1,3))
					except KeyboardInterrupt:
						print()
						print("KeyboardInterrupt")
						sys.exit(1)
					except:
						cve.clear()
						continue

				cursor.close()
				db.close()

			elif opt in ["-e","edb"]:

				print("parsing options...")
				try:
					page_start = int(arg.split("-")[0])
					page_end = int(arg.split("-")[1])

					if page_start < 1 or page_end < 1 or page_end < page_start:
						print("Invalid page ",arg)
						sys.exit(1)
				except:
					print("Invalid page ",arg)
					sys.exit(1)

				import pymysql
				print("loading database configure...")
				try:
					conf = open(config, "rb")
					conf_dict = pickle.load(conf)
					conf.close()
				except:
					print('\033[31mDatabase configure load failed\033[0m')
					sys.exit(1)
				print("connecting to database...")
				try:
					db = pymysql.connect(host = conf_dict["database"]["host"], port = 3306, user = conf_dict["database"]["user"], password = conf_dict["database"]["password"], db = conf_dict["database"]["db"], charset = 'utf8')
					cursor = db.cursor()
				except pymysql.Error:
					print('\033[31mDatabase connect failed\033[0m')
					sys.exit(1)
				except KeyError:
					print('\033[31mThere is no connectable database\033[0m')
					print("Try 'CVE_spider database -c' to connect a database")
					sys.exit(1)

				from CVE_crawler import EDBCrawler
				import time, random, math
				print("initializing edb_spider...")
				edb = EDBCrawler()
				#bar = pyprind.ProgBar((page_end - page_start + 1) * 50)
				print("scrapy...")
				for page in range(page_start, page_end + 1):
					try:
						num = -1
						for i in edb.get_edb_id_by_page(page):
							try:
								num += 1

								#print bar
								print(" [", end='')
								bar = ""
								for j in range(0, math.floor(((page-page_start)+num/50)/(page_end-page_start+1)*50)):
									bar += "#"
								print(bar, end='')
								bar = ""
								for j in range(0, 50-math.floor(((page-page_start)+num/50)/(page_end-page_start+1)*50)):
									bar += " "
								print(bar, end='')
								print("]", end='')
								print("%.02f%1s"% (((page-page_start)+num/50)/(page_end-page_start+1)*100,"%"), end='')
								print(" Page:"+str(page), end='')
								print(" ID:"+i+"    ", end='\r')

								#check database
								sql = "SELECT `EDB_ID` FROM `exploit` WHERE `EDB_ID`=" + str(i) + " LIMIT 1;"
								if cursor.execute(sql) != 0:
									edb.clear()
									continue
								if not edb.set_target_edb(str(i)):
									edb.clear()
									continue

								result = edb.get_edb_info()
								sql = "INSERT INTO `exploit` (`EDB_ID`, `title`, `author`, `publish`, `CVE_ID`, `type`, `platform`, `code`) VALUES ("+str(result[0])+", '"+str(result[1])+"', '"+str(result[2])+"', '"+str(result[3].date())+"', '"+str(result[4])+"', '"+str(result[5])+"', '"+str(result[6])+"', '"+str(result[7])+"');"
								cursor.execute(sql)
								db.commit()
								edb.clear()
							except KeyboardInterrupt:
								print()
								print("KeyboardInterrupt")
								sys.exit(1)
							except:
								edb.clear()
								continue
					except KeyboardInterrupt:
						print()
						print("KeyboardInterrupt")
						sys.exit(1)
					except:
						print("Page ",page," get failed")
						print("Please try again latter")
						sys.exit(1)
				cursor.close()
				db.close()
				print(" [", end='')
				bar = ""
				for j in range(0, 50):
					bar += "#"
				print(bar, end='')
				print("]", end='')
				print("%.02f%1s"% (100.0,"%"), end='')
				print(" EDB ID : "+i+"      ", end='\n')

			else:
				assert False,opt

	else:
		assert False,sys.argv[1]