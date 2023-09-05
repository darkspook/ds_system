from django.shortcuts import render
import random
import calendar
import json
import csv

def tree(request):

	def build_family_tree(member, family_members):
		if member['name'] in family_members:
			member['children'] = family_members[member['name']]
			for child in family_members[member['name']]:
				build_family_tree(child, family_members)

	csv_file = 'portfolio/static/portfolio/tree.csv'
	data = []

	# Read the CSV file and store data in dictionaries
	with open(csv_file, 'r') as file:
		csv_reader = csv.DictReader(file)
		for row in csv_reader:
			if row['fullname'] is '':
				row['fullname'] = row['name']

			# Replace '+' with '†' in name and fullname
			# row['name'] = row['name'].replace('+', '†')
			# row['fullname'] = row['fullname'].replace('+', '†')
			# row['parent'] = row['parent'].replace('+', '†')
			# if 'bday' in row:
			# 	row['fullname'] = f"{row['fullname']}<br>{row['bday']}"
			# 	del row['bday']

			data.append(row)

			# print('DATA: ',data)
	file.close()

	# Create a dictionary to store members
	family_members = {}

	# Organize the data into the family members dictionary
	for item in data:
		parent = item.get('parent')
		# if parent is '':
		if parent is '' or parent == item['name']:
			# This is a top-level member or a parent with themselves as a child
			family_members[item['name']] = []
		else:
			if parent not in family_members:
				family_members[parent] = []
			family_members[parent].append(item)

	# Find top-level members
	top_level_members = [member for member in data if member['parent'] not in family_members]

	# Build the family tree
	for top_member in top_level_members:
		build_family_tree(top_member, family_members)

	for member in data:
		# Remove the "parent" key from all members
		member.pop('parent', None)
		# Replace '+' with '†' in the "name" and "fullname" fields
		member['name'] = member['name'].replace('+', '†')
		member['fullname'] = member['fullname'].replace('+', '†')

	final_data = top_level_members

	# print('FINAL DATA: ',final_data)
	json_tree = json.dumps(final_data, indent=2)
	# json_tree = json.dumps(final_data)
	# json_tree = json.dumps(data, ensure_ascii=False) #special characters
	context = {'json_tree': json_tree[1:-1]}
	# context = {'json_tree': json_tree}
	# print('JSON DATA: ',json_tree[1:-1])

	return render(request, 'portfolio/tree.html', context)

def dutygenerator(request):
	print("Inside dutygenerator")
	# print(request.GET['selectMonth'])
	print(request.GET.get('selectMonth'))
	print(request.GET.get('inputYear'))
	if request.GET.get('selectMonth') is not None and request.GET.get('inputYear') is not None:

		# List of personnel 29
		duty_personnel = {}
		total_personnel = 27+1
		personnel = list(range(1, total_personnel)) #29 personnel
		exempted_personnel = [0]; #list of exempted personnel
		# print(f"Exempted personnel {exempted_personnel}")
		# print(len(personnel))
		# Initialize calendar and shuffle personnel list
		cal = calendar.Calendar(firstweekday=calendar.SUNDAY)
		personnel = [item for item in personnel if item not in exempted_personnel] #remove exempted from the list
		# print(f"Personnel after removing exempted {personnel}")
		random.shuffle(personnel)

		# print(personnel)
		month = int(request.GET.get('selectMonth'))
		year = int(request.GET.get('inputYear'))

		# Initialize counters for number of personnel selected for the week and weekend
		# weekday_count = 0
		# weekend_count = 0

		# Iterate through each day of the month
		for day in cal.itermonthdays2(year, month):
			# If it's not a valid day, skip
			if day[0] == 0:
				continue

		    # If it's a weekday
			if day[1] < 5:
				if len(personnel)<2:
					# print("Weekdays, available personnel is less than 2, RESET!")
					personnel = list(range(1, 28))
					personnel = [item for item in personnel if item not in exempted_personnel] #remove exempted from the list
					random.shuffle(personnel)
		        # Select two personnel randomly and remove them from the list
				selected_personnel = random.sample(personnel, 2)
				for p in selected_personnel:
					personnel.remove(p)
			
		    # If it's a weekend
			else:
				if len(personnel)<4:
					# print("Weekend, available personnel is less than 4, RESET!")
					personnel = list(range(1, 28))
					personnel = [item for item in personnel if item not in exempted_personnel] #remove exempted from the list
					random.shuffle(personnel)
		        # Select four personnel randomly and remove them from the list
				selected_personnel = random.sample(personnel, 4)
				for p in selected_personnel:
					personnel.remove(p)

			# if len(personnel)<4:
			# 	print("personnel is less than 4, RESET!")
			# 	personnel = list(range(1, 30))
			# 	random.shuffle(personnel)
			# print(f"Remaining personnel: {personnel}")
		    # Print selected personnel for the day
			# print(f"Day {day[0]}: {selected_personnel}")
		    # print(f"Length {len(selected_personnel)}")

			if len(selected_personnel)==4:
				duty_personnel[day[0]] = translatepersonnel(selected_personnel[0]),translatepersonnel(selected_personnel[1]),translatepersonnel(selected_personnel[2]),translatepersonnel(selected_personnel[3])
				# print(f"{day[0]} {calendar.month_name[month]} {year}\n{translatepersonnel(selected_personnel[0])}\n{translatepersonnel(selected_personnel[1])}\n{translatepersonnel(selected_personnel[2])}\n{translatepersonnel(selected_personnel[3])}\n")
			else:
				duty_personnel[day[0]] = translatepersonnel(selected_personnel[0]),translatepersonnel(selected_personnel[1])
				# print(f"{day[0]} {calendar.month_name[month]} {year}\n{translatepersonnel(selected_personnel[0])}\n{translatepersonnel(selected_personnel[1])}\n")
			
			# print(f"Selected personnel: {selected_personnel}")

			
		# print(duty_personnel)

		context = {
			# 'day':day[0],
			'month':calendar.month_name[month],
			'year':year,
			'personnel':duty_personnel,
		}
		# print(f"Context: {context}")
		return render(request, 'portfolio/duty_generated.html', context)

	else:
		return render(request, 'portfolio/duty_generator.html')
	

personnel_dict = {
	1:"Jessar B. Adornado",
	2:"Julius Christopher B. Arroyo",
	3:"Sherry Ann B. Balingit",
}


def translatepersonnel(personnel):
	if personnel == 1:
		return "Julius Christopher B. Arroyo"
	elif personnel == 2:
		return "Sherry Ann B. Balingit"
	elif personnel == 3:
		return "Sarahlyn B. Bendaña"
	elif personnel == 4:
		return "Akim S. Berces"
	elif personnel == 5:
		return "Ronel R. Bernardino"
	elif personnel == 6:
		return "Efren D. Binamira Jr."
	elif personnel == 7:
		return "Joya P. De La Rama"
	elif personnel == 8:
		return "Jeric M. De La Rosa"
	elif personnel == 9:
		return "Lanilyn C. Esquivel"
	elif personnel == 10:
		return "Lourdes M. Francisco"
	elif personnel == 11:
		return "Frenlie Micah F. Guiriba"
	elif personnel == 12:
		return "Kristeen C. Lim"
	elif personnel == 13:
		return "Raymund John Tomas D. Lorilla"
	elif personnel == 14:
		return "Joy M. Lotrinia"
	elif personnel == 15:
		return "Karla Thea O. Manlangit"
	elif personnel == 16:
		return "Chat C. Mimay"
	elif personnel == 17:
		return "Gian Carlo A. Molina"
	elif personnel == 18:
		return "Ronna Faith M. Naz"
	elif personnel == 19:
		return "Rodel M. Mortega"
	elif personnel == 20:
		return "Marian Mae S. Navarra"
	elif personnel == 21:
		return "Gremil Alexis A. Naz"
	elif personnel == 22:
		return "Ma. Angelica A. Precones"
	elif personnel == 23:
		return "Marlopredan B. Tandog"
	elif personnel == 24:
		return "Joan D. Vergara"
	elif personnel == 25:
		return "Ruffa G. Belga"
	elif personnel == 26:
		return "Jovel N. Loreto"
	elif personnel == 27:
		return "Ma. Ires J. Galido"
	# elif personnel == 26:
	# 	return "Vergara"
	# elif personnel == 26:
	# 	return "Vergara"
	# elif personnel == 26:
	# 	return "Vergara"
	# elif personnel == 26:
	# 	return "Vergara"

def home(request):
	return render(request, 'portfolio/home.html')

def welcome(request):
	return render(request, 'portfolio/welcome.html')

def about(request):
	return render(request, 'portfolio/about.html')

def projects(request):
	return render(request, 'portfolio/projects.html')

def contact(request):
	return render(request, 'portfolio/contact.html')