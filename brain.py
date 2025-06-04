import json
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import csv


class Calculator:
	def __init__(self, meal_100, weight):
		self.meal_100 = meal_100
		self.weight = weight
		self.meal = {}
		self.consumed={}
		self.macro_p={}
		self.calculate_meal()
		self.calculate_calories()
		self.calculate_macro()
		self.add_to_menu()
		
	def calculate_meal(self):
		for key in self.meal_100.keys():
			if key != "name":
				self.meal[key] = float(self.meal_100[key])*self.weight/100
			else:
				self.meal_name = self.meal_100[key]
				
	def calculate_calories(self):
		with open("cal_consumed.json", mode="r+", encoding="UTF-8") as file_calories:
			self.calories=json.load(file_calories)
			
			for key in self.calories.keys():
				self.consumed[key] = self.calories[key] + self.meal[key]
			if self.consumed["cal"]>=950:
				print("target reached!")
			
			file_calories.seek(0)
			file_calories.truncate()
			json.dump(self.consumed, file_calories)

	def calculate_macro(self):
		self.total_macro = sum(list(self.consumed.values())[1:4])
		for key in list(self.consumed.keys())[1:4]:
			if self.total_macro == 0:
				self.macro_p[key] = 0
			else:
				self.macro_p[key] = round(100*self.consumed[key]/self.total_macro) 
	
	def add_to_menu(self):
		new_item = {'name':self.meal_name}
		new_item = new_item|self.meal
		with open("menu.csv", mode="a", newline='') as menu_file:
			writer = csv.DictWriter(menu_file, fieldnames=new_item.keys())
			writer.writerow(new_item)
			
	
	@staticmethod
	def add_new_custom(new_meal):
		new_meal = new_meal
		with open ('meals_per_100.csv', mode='a', newline='') as meals_100_file:
			writer = csv.DictWriter(meals_100_file, fieldnames=new_meal.keys())
			writer.writerow(new_meal)
			
	@staticmethod
	def goal():
		with open("goal.json", mode="r", encoding="UTF-8") as goal_file:
			return int(json.load(goal_file)["goal"])

	@staticmethod
	def change_goal(goal):
		new_goal = {"goal":goal}
		with open("goal.json", mode="w") as goal_file:
			json.dump(new_goal, goal_file)
			
	@staticmethod
	def items_in_menu():
		with open ('menu.csv', mode='r', newline='') as menu_file:
			items = csv.DictReader(menu_file)
			return list(items)
			

class Scraper:
	def __init__(self,entry):
		self.options = Options()
		self.options.add_argument("--headless")
		self.service = Service("/usr/local/bin/geckodriver")
		self.driver = webdriver.Firefox(service=self.service, options=self.options)
		self.search_food(entry)
	
	def search_food(self, entry):
		self.page = self.driver.get("https://www.tablycjakalorijnosti.com.ua/tablytsya-yizhyi")
		self.search_input = self.driver.find_element(By.ID, "search-input")
		self.search_input_input = self.search_input.find_element(By.TAG_NAME, "input")
		self.search_input_input.send_keys(entry)
		time.sleep(1)
		self.get_suggestions()
	
	def get_suggestions(self):
			self.suggestions = self.driver.find_elements(By.CSS_SELECTOR, "a.p-link")
			self.suggestions = self.suggestions[:10]
			self.meal_calories = []
			self.suggestions_t = []
			
			for i in range(len(self.suggestions)):
				self.calories = self.driver.find_elements (By.CSS_SELECTOR, "tbody td.hide-xs.md-cell:not(.ng-hide)")
				self.suggestions_t.append(self.suggestions[i].text)
				self.meal_calories.append(self.calories[i].text)
			self.suggestion = dict(zip(self.suggestions_t, self.meal_calories))
			
	def suggestion_selected(self, selector):
			for i in range(len(self.suggestions)):
				if self.suggestions[i].text == selector:
					self.suggestions[i].click()
					break
			self.macro_find = self.driver.find_elements(By.CSS_SELECTOR, ".block-background."
														"flex-xs-auto.flex-sm-auto .text-subtitle."
														"layout-align-start-center.layout-row span")
			self.macro = [el.text for el in self.macro_find[:3]]
			
	def driver_quit(self):
			self.driver.quit()
	
