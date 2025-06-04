import tkinter as tk
import brain
import csv

class MainWindow(tk.Tk):
	def __init__(self):
		super().__init__()
		self.setup_main_window()
		self.create_frame_1()
		self.create_frame_1_top()
		self.add_elements_frame_1_top()
		self.create_frame_1_bot()
		self.add_elements_frame_1_bot()
		self.create_frame_2()
		self.create_frame_2_top()
		self.add_elements_frame_2_top()
		self.create_frame_2_bot()
		self.add_elements_frame_2_bot()
		self.chosen = False
		self.scraper = None
		
		self.mainloop()
		
		
	@staticmethod
	def generate_grid(widget, rows, columns, weight_r=1, weight_c=1):
		for i in range (rows):
			widget.rowconfigure(i, weight=weight_r)
			for j in range(columns):
				widget.columnconfigure(j, weight=weight_c)
			
		
	def setup_main_window(self):
		self.geometry("800x500")
		self.title("Calorie tracker")	
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=4)
		self.columnconfigure(1, weight=6)
		
	def create_frame_1(self):
		self.frm_1 = tk.Frame(self)	
		#grid_section:
		self.frm_1.grid(row=0, column=0, sticky="news")
		self.generate_grid(self.frm_1, 2, 1)
		
	def create_frame_1_top(self):
		self.frm_1_top = tk.Frame(self.frm_1)
		#grid_section:
		self.frm_1_top.grid(row=0, column=0, sticky="news")
		self.generate_grid(self.frm_1_top, 7, 12)
			
	def add_elements_frame_1_top(self):
		self.lbl_goal = tk.Label(self.frm_1_top, text=f'YOUR GOAL:\n{brain.Calculator.goal()}',
						 		 relief="groove", borderwidth=2, font=24)
		self.btn_change = tk.Button(self.frm_1_top, text="Set Goal", command=self.set_goal)
		self.btn_weekly = tk.Button(self.frm_1_top, text="Weekly\noverview")
		#grid_section:
		self.lbl_goal.grid(row=2, column=1, rowspan=4, 
						   columnspan=6, sticky="news")
		self.btn_change.grid(row=6, column=3, sticky="e")
		self.btn_weekly.grid(row=3, column=8, sticky="news",
							 rowspan=2, columnspan=2,)
		
	def create_frame_1_bot(self):
		self.frm_1_bot = tk.Frame(self.frm_1)
		#grid_section:
		self.frm_1_bot.grid(row=1, column=0,  sticky="news")
		self.generate_grid(self.frm_1_bot, 7, 12)
			
	def add_elements_frame_1_bot(self):
		self.lbl_today = tk.Label(self.frm_1_bot, text="Today")
		self.btn_menu = tk.Button(self.frm_1_bot, text="menu", command=self.on_menu_clicked)
		self.lbl_graph = tk.Label(self.frm_1_bot, text="Graph")
		self.btn_new_day = tk.Button(self.frm_1_bot, text="change to image")
		#grid_section:
		self.lbl_today.grid(row=1, column=7, sticky="news")
		self.btn_menu.grid(row=0, column=11, sticky="es")
		self.lbl_graph.grid(row=3, column=1, sticky="news", 
							rowspan=3, columnspan=6)
		self.btn_new_day.grid(row=5, column=11, sticky="news")
		
	def create_frame_2(self):	
		self.frm_2 = tk.Frame(self)
		#grid_section:
		self.frm_2.grid(row=0, column=1, sticky="news", padx=(10,0))
		self.generate_grid(self.frm_2, 2, 1)
		
	def create_frame_2_top(self):
		self.frm_2_top = tk.Frame(self.frm_2)
		#grid_section:
		self.frm_2_top.grid(row=0, column=0, sticky="news")
		self.generate_grid(self.frm_2_top, 4, 2) 
		
	def add_elements_frame_2_top(self):
		self.lbl_food_name = tk.Label(self.frm_2_top, text="Enter the name" 
							 " of the meal,a food item or an ingridient:")
		self.lbl_warning = tk.Label(self.frm_2_top, fg="red", text="")
		self.ent_name = tk.Entry(self.frm_2_top, font=12)
		self.btn_confirm = tk.Button(self.frm_2_top, text="Confirm",
									 command=self.on_confirm_clicked)
		self.btn_custom = tk.Button(self.frm_2_top, text="Add new food", command=self.on_add_new_clicked)
		#grid_section:
		self.btn_custom.grid(row=0, column=0, sticky="e", pady=(5,0))
		self.lbl_food_name.grid(row=1, column=0, sticky="sw")
		self.ent_name.grid(row=2, column=0, sticky="ew", ipady=1)
		self.btn_confirm.grid(row=2, column=1, sticky="w")
		self.lbl_warning.grid(row=3, column=0, sticky="nw")
			
	def create_frame_2_bot(self):
		self.frm_2_bot = tk.Frame(self.frm_2)
		#grid_section:
		self.frm_2_bot.grid(row=1, column=0,  sticky="news")
		self.generate_grid(self.frm_2_bot, 10, 1)
		
	def add_elements_frame_2_bot(self):
		for w in self.frm_2_bot.winfo_children():
			w.destroy()
		for i in range(10):
			lbl=tk.Label(self.frm_2_bot, text='     ', fg='blue', font=12)
			lbl.grid(row=i, column=0, sticky="w")
	
	#functionality_section
	
	def on_confirm_clicked(self):
		meal_name = self.ent_name.get()
		self.item_check(meal_name)
		
	def item_check(self, meal_name):
		self.meal_name = meal_name
		with open ('meals_per_100.csv', mode='r+',newline='') as meals_100_file:
			meals_100 = csv.DictReader(meals_100_file)
			self.found = False
			for meal_found in meals_100:
				if self.meal_name == meal_found['name']:
					self.lbl_warning.config(text="")
					self.meal_100=meal_found
					if self.scraper:
						self.scraper.driver_quit()
						self.scraper = None
					weight_window = WeightWindow()
					self.found = True
					break
			if (not self.found) and (not self.chosen):
				self.lbl_warning.config(fg="red",text="Please, choose from suggestions or add custom meal")
				self.suggest_on_confirm()
			elif (not self.found) and (self.chosen):
				self.scraper.suggestion_selected(self.meal_name)
				self.add_elements_frame_2_bot()
				macro = {'carb':self.scraper.macro[0],'pro':self.scraper.macro[1],'fat':self.scraper.macro[2]}
				for key, value in self.suggestor.items():
					if key == self.meal_name:
						item = {'name':key,'cal':value}
						break	
				new_meal = item|macro
				brain.Calculator.add_new_custom(new_meal)
				self.chosen = False
				self.item_check(self.meal_name)
				
	def on_add_new_clicked(self):
		add_food_window = AddFoodWindow() 
	
	def suggest_on_confirm(self):
		if not self.scraper:
			self.scraper = brain.Scraper(self.meal_name)
		else:
			self.scraper.search_food(self.chosen)
		self.suggestor = self.scraper.suggestion
		for w in self.frm_2_bot.winfo_children():
			w.destroy()
		for i, (key, item) in enumerate(self.suggestor.items()):
			lbl=tk.Label(self.frm_2_bot, text=f'{key} - {item}', fg='blue', font=12)
			lbl.grid(row=i, column=0, sticky="w")
			lbl.bind("<Button-1>", self.on_label_clicked)


	def on_label_clicked(self,event):
		label_clicked = event.widget
		meal_name = label_clicked.cget("text")
		for item in self.suggestor.values():
			if f' - {item}' in meal_name:
				meal_name = meal_name.replace(f' - {item}','')
		self.chosen = True
		self.item_check(meal_name)
		
	def set_goal(self):
		set_new = ChangeGoalWindow()
		self.lbl_goal.configure(text=f'YOUR GOAL:\n{brain.Calculator.goal()}')

	def on_menu_clicked(self):
		self.menu_window = MenuWindow()
		
class WeightWindow(tk.Toplevel):
	def __init__(self):
		super().__init__()
		
		self.weight = None
			
		MainWindow.generate_grid(self, 3, 1)
		self.lbl_weight_t = tk.Label(self, text="How much did you it?")
		self.ent_weight = tk.Entry(self)
		self.lbl_weight_r = tk.Label(self)
		self.btn_weight_ok = tk.Button(self, text="Ok", command=self.on_ok_clicked)
		self.btn_weight_c = tk.Button(self, text="Cancel", command=self.on_cancel_clicked)
		#grid_section
		self.ent_weight.grid(row=1, column=0, columnspan=2, sticky="news")
		self.lbl_weight_t.grid(row=0, column=0, sticky="ws")
		self.lbl_weight_r.grid(row=1, column=2, sticky="wns")
		self.btn_weight_ok.grid(row=2, column=0, sticky="news")
		self.btn_weight_c.grid(row=2, column=2, sticky="news")
		
		self.transient(self.master)
		self.grab_set()
		self.wait_window(self)
		
	def on_ok_clicked(self):
		self.weight = self.ent_weight.get()
		try:
			self.weight = float(self.weight)
			calc = brain.Calculator(self.master.meal_100, self.weight)
			self.destroy()
		except ValueError:
			self.ent_weight.delete(0, tk.END)
			return 
				
	def on_cancel_clicked(self):
		self.destroy()
		
class AddFoodWindow(tk.Toplevel):
	def __init__(self):
		super().__init__()
		self.title("Add Food")
		MainWindow.generate_grid(self, 3, 5)
		
		self.lbl_name = tk.Label(self, text="Name of the meal:")
		self.ent_name = tk.Entry(self, font=12)
		self.lbl_cal = tk.Label (self, text="calories/100%:")
		self.ent_cal = tk.Entry(self, font=12)
		self.lbl_carbs = tk.Label (self, text="carbs/100%:")
		self.ent_carbs = tk.Entry(self, font=12)
		self.lbl_pro = tk.Label (self, text="protein/100%:")
		self.ent_pro = tk.Entry(self, font=12)
		self.lbl_fat = tk.Label (self, text="fat/100%:")
		self.ent_fat = tk.Entry(self, font=12)
		self.btn_ok = tk.Button(self, text="Ok", command=self.on_ok_clicked)
		self.btn_c = tk.Button(self, text="Cancel", command=self.on_cancel_clicked)
		#grid_section
		self.lbl_name.grid(row=0, column=0, columnspan=4, sticky="sw")
		self.ent_name.grid(row=1, column=0, columnspan=4, sticky="news")
		self.lbl_cal.grid(row=2, column=0, sticky="news")
		self.ent_cal.grid(row=2, column=1, sticky="news")
		self.lbl_carbs.grid(row=2, column=2, sticky="news")
		self.ent_carbs.grid(row=2, column=3, sticky="news")
		self.lbl_pro.grid(row=3, column=0, sticky="news")
		self.ent_pro.grid(row=3, column=1, sticky="news")
		self.lbl_fat.grid(row=3, column=2, sticky="nes")
		self.ent_fat.grid(row=3, column=3, sticky="news")
		self.btn_ok.grid(row=2, column=5, sticky="news", padx=3)
		self.btn_c.grid(row=3, column=5, sticky="news",padx=3)
		
		self.transient(self.master)
		self.grab_set()
		self.wait_window(self)
		
	def on_ok_clicked(self):
		self.new_meal = {'name':self.ent_name.get(),'cal':self.ent_cal.get(),
					  'carb': self.ent_carbs.get(), 'pro': self.ent_pro.get(),
					  'fat' :self.ent_fat.get()}
		try:
			for i in list(self.new_meal)[1:5]:
				self.new_meal[i] = float(self.new_meal[i])	
			self.destroy()
		except ValueError:
			return 
		
		brain.Calculator.add_new_custom(self.new_meal)			
							
	def on_cancel_clicked(self):
		self.destroy() 	

class ChangeGoalWindow(tk.Toplevel):
	
	def __init__(self):
		super().__init__()
		
		self.title('Set Goal')
		self.lbl = tk.Label(self, text='Set new goal:')
		self.ent = tk.Entry(self)
		self.btn = tk.Button(self, text="OK", command=self.on_ok_clicked)
		self.lbl.pack(fill=tk.BOTH, expand=True)
		self.ent.pack(fill=tk.BOTH, expand=True)
		self.btn.pack(fill=tk.BOTH, expand=True)
		
		self.transient(self.master)
		self.grab_set()
		self.wait_window(self)
		
	def on_ok_clicked(self):
		goal = self.ent.get()
		try:
			goal = int(goal)
			brain.Calculator.change_goal(goal)
			self.destroy()
		except ValueError:
			self.ent.delete(0, tk.END)	
			
class MenuWindow(tk.Toplevel):
	def __init__(self):
		super().__init__()
		self.title('Menu')
		self.get_items()
		self.build()
		
		self.transient(self.master)
		self.grab_set()
		self.wait_window(self)
		
	def build(self):
	
		for w in self.winfo_children():
			w.destroy()
			
		self.master.generate_grid(self, 2, self.rows)
		
		for index,row in enumerate(self.items):
			self.lbl = tk.Label(self, text=f'{index+1}. {row["name"]}:'
							    f' {row["cal"]}kcal, {row["carb"]}g carbs,' 
							    f' {row["pro"]}g protein, {row["fat"]}g fat')
			self.lbl.grid(row=index, column=0, sticky="news")
			
			self.btn = tk.Button(self, text="del", command=lambda l=index: self._on_delete(l))
			self.btn.grid(row=index, column=1, sticky="news", padx=3)
			
	def _on_delete(self, index):
		self.items.pop(index)
		with open('menu.csv', 'w', newline='') as f:
			if self.items:
				writer = csv.DictWriter(f, fieldnames=self.items[0].keys())
				writer.writeheader()
				writer.writerows(self.items)
			else:
  				writer = csv.writer(f)
  				writer.writerow(['name','cal','carb','pro','fat'])
		self.get_items()
		self.build()
		
	def get_items(self):
		self.items = brain.Calculator.items_in_menu()
		self.rows = len(self.items)
			
main = MainWindow()
