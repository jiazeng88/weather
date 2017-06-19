from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import sys

def get_city_and_state(str):
	city, state=str.split(", ")
	print "Looking up weather for %s city in %s state" %(city, state)
	
def done_city_and_state(str):
	city, state=str.split(", ")
	print "Exiting weather session for %s city in %s state" %(city, state)	
	
class WeatherPoller:

	def __init__(self, location):
		self.location = location
		self.drv = webdriver.Chrome()
		self.drv.get("http://www.weather.com")
		self.wait = WebDriverWait(self.drv, 30)
		
	def close(self):
		done_city_and_state(self.location)
		self.drv.quit()

	def get_single_item(self, info, infotype):
		if infotype == "temperature":
			if re.search("F", info):
				self.unit = "F"
			elif re.search("C", info):
				self.unit = "C"
			else:
				self.unit = "?"

		ret_val = info.split()[0]
		re.sub("u\'", "", ret_val)
		#re.sub("\xb0", "", ret_val) degree symbol
		re.sub("'", "", ret_val)
		return ret_val

	def enter_location(self):
		get_city_and_state(self.location)
		elem = self.drv.find_element_by_name("search")
		if elem.text != "":
			elem.clear()
			time.sleep(5)

		elem.send_keys(self.location)
		elem.send_keys(Keys.RETURN)

	def get_info(self):
		#target_list = ["temperature","weather-phrase","actual-hi-temp","actual-lo-temp"]
		target_list = {"temperature":"today_nowcard-temp", "weather-phrase":"today_nowcard-phrase"}
		for ele in target_list.keys():
			self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, target_list[ele])))
			info = self.drv.find_element_by_class_name(target_list[ele]).text
			result = self.get_single_item(info,target_list[ele])
			print "%s is %s" %(ele, result)	

def usage():
	print 'Usage: <python> %s "Location(City|Town, State)" ' %(__file__)
			
if __name__ == "__main__":
	if (len(sys.argv)!=2):
		usage()
		sys.exit(2)
	weather = WeatherPoller(sys.argv[1])	
	weather.enter_location()
	weather.get_info()
	weather.close()
