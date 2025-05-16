import json
TARGET_CAL = 950
CARB=45
PRO=30
FAT=25

def cal_left(cal_consumed):
	return TARGET_CAL - cal_consumed[0]
	
def macro_f(carb,pro,fat,carb_consumed,pro_consumed,fat_consumed):
	total_macro=carb_consumed+pro_consumed+fat_consumed
	carb_p=100*carb_consumed/total_macro
	pro_p=100*pro_consumed/total_macro
	fat_p=100*fat_consumed/total_macro
	macro_list=[round(carb_p),round(pro_p),round(fat_p)]
	return macro_list
	
def cal_sum(cal,carb,pro,fat):
	with open("cal_consumed.json", mode="r+", encoding="UTF-8") as file_calories:
		calories=json.load(file_calories)
		cal_consumed=calories["cal_consumed"]+cal
		carb_consumed=calories["carb"]+carb
		pro_consumed=calories["pro"]+pro
		fat_consumed=calories["fat"]+fat
		result=macro_f(carb,pro,fat,carb_consumed,pro_consumed,fat_consumed)
		if cal_consumed>=TARGET_CAL:
			print("target reached!")
		calories["cal_consumed"]=cal_consumed
		calories["carb"]=carb_consumed
		calories["pro"]=pro_consumed
		calories["fat"]=fat_consumed
		file_calories.seek(0)
		file_calories.truncate()
		json.dump(calories, data_file)
		cal_consumed=[cal_consumed]+result
	return cal_consumed
		
cal = int(input('cal:'))
carb = int(input('carb:'))
pro = int(input('pro:'))
fat = int(input('fat:'))
cal_consumed=cal_sum(cal,carb,pro,fat)		

print(f"calories consumed: {cal_consumed[0]}")
print(f"left to goal: {cal_left(cal_consumed)}")
print(f"carbs:{cal_consumed[1]}")
print(f"pro:{cal_consumed[2]}")
print(f"fat:{cal_consumed[3]}")
r=input("Do you want to reset? y/n:")
if r == "y":
	with open("cal_consumed.json", mode="r+", encoding="UTF-8") as file_calories:
		calories=json.load(file_calories)
		for key in calories.keys():
			calories[key]=0
		file_calories.seek(0)
		file_calories.truncate()
		json.dump(calories, data_file, indent=4)
