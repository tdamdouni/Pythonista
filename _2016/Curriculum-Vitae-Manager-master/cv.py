"""
CV Generator.

Johann du Toit - South-Africa
https://github.com/Johanndutoit
"""
from __future__ import print_function

import io, os, sys, urllib, time
from xml.dom.minidom import parse, parseString
from datetime import date, datetime
from time import mktime

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *

# Read in all the information

print("CV Generator - The easy way to build and update a cv")
print("v0.0.1 - Johann du Toit (South-Africa , Roar!!!!)")
print("=====================================================")

if len(sys.argv) <= 2:
	# Oops no data file exit now!
	print("Specify a Data XML file and a Output filename!")
	sys.exit(0)

# Read the Data XML File
data_xml_document = parse(sys.argv[1])

# Get the Root Element
dom_root_element = data_xml_document.getElementsByTagName('cvdata')[0]

# Get the Name/E-Mail etc.
cv_name = dom_root_element.getElementsByTagName('name')[0].firstChild.data
cv_email = dom_root_element.getElementsByTagName('email')[0].firstChild.data
cv_cover_letter = dom_root_element.getElementsByTagName('letter')[0].firstChild.data

# Parse the Born Date
dom_dob_element = dom_root_element.getElementsByTagName('dob')[0]
cv_dob_year = dom_dob_element.getAttribute('year')
cv_dob_month = dom_dob_element.getAttribute('month')
cv_dob_date = dom_dob_element.getAttribute('day')

# Parse the Addresses
cv_residential_addresses = []
cv_postal_addresses = []

# Load the Residential Addresses
for residential_addr in dom_root_element.getElementsByTagName('address')[0].getElementsByTagName('residential'):
	cv_residential_addresses.append(residential_addr.firstChild.data)

# Load the Postal Addresses
for postal_addr in dom_root_element.getElementsByTagName('address')[0].getElementsByTagName('postal'):
	cv_postal_addresses.append(postal_addr.firstChild.data)

# Parse the Contact Numbers and load them into this array
cv_contact_numbers = []

# Load the Contact Numbers (TEL)
for tel_numb in dom_root_element.getElementsByTagName('contactnumbers')[0].getElementsByTagName('tel'):
	contact_number = {}
	contact_number["type"] = "tel"
	contact_number["number"] = tel_numb.firstChild.data
	cv_contact_numbers.append(contact_number)

# Load the Contact Numbers (CEL)
for cel_numb in dom_root_element.getElementsByTagName('contactnumbers')[0].getElementsByTagName('cel'):
	contact_number = {}
	contact_number["type"] = "cel"
	contact_number["number"] = cel_numb.firstChild.data
	cv_contact_numbers.append(contact_number)

# Load the Contact Numbers (FAX)
for fax_numb in dom_root_element.getElementsByTagName('contactnumbers')[0].getElementsByTagName('fax'):
	contact_number = {}
	contact_number["type"] = "fax"
	contact_number["number"] = fax_numb.firstChild.data
	cv_contact_numbers.append(contact_number)

# Parse the users accounts
cv_accounts = []
for account_element in dom_root_element.getElementsByTagName('accounts')[0].getElementsByTagName('account'):
	account_obj = {}
	account_obj["name"] = account_element.getElementsByTagName('name')[0].firstChild.data
	account_obj["url"] = account_element.getElementsByTagName('url')[0].firstChild.data
	# account_obj["logo"] = account_element.getElementsByTagName('logo')[0].data
	cv_accounts.append(account_obj)

# Parse the Skills that we use to create a Skill Matrix
cv_skills = []
for skill_element in dom_root_element.getElementsByTagName('skills')[0].getElementsByTagName('skill'):
	skill_obj = {}
	skill_obj["rating"] = skill_element.getAttribute('rating')
	skill_obj["name"] = skill_element.firstChild.data
	cv_skills.append(skill_obj)

# Load the Contact Numbers (TEL)
cv_school_name = dom_root_element.getElementsByTagName('school')[0].getElementsByTagName('name')[0].firstChild.data
cv_school_year = dom_root_element.getElementsByTagName('school')[0].getElementsByTagName('year')[0].firstChild.data
cv_distinctions = []

# Loop Distinctions
for distinction_element in dom_root_element.getElementsByTagName('school')[0].getElementsByTagName('distinctions')[0].getElementsByTagName('distinction'):
	cv_distinctions.append(distinction_element.firstChild.data)

# Parse all the Education of the User (Certifications etc.)
cv_education = []
for edu_element in dom_root_element.getElementsByTagName('education')[0].getElementsByTagName('edu'):
	education_obj = {}
	education_obj["name"] = edu_element.getElementsByTagName('name')[0].firstChild.data
	education_obj["logo"] = edu_element.getElementsByTagName('logo')[0].firstChild.data
	education_obj["timeframe"] = edu_element.getElementsByTagName('timeframe')[0].firstChild.data
	education_obj["description"] = edu_element.getElementsByTagName('description')[0].firstChild.data
	cv_education.append(education_obj)

# Parse Work Experience
cv_experience = []

# Load Working Experience
for company_experience_element in dom_root_element.getElementsByTagName('experience')[0].getElementsByTagName('company'):
	company_obj = {}
	company_obj["type"] = "company"
	company_obj["name"] = company_experience_element.getElementsByTagName('name')[0].firstChild.data
	company_obj["logo"] = company_experience_element.getElementsByTagName('logo')[0].firstChild.data
	company_obj["tel"] = company_experience_element.getElementsByTagName('tel')[0].firstChild.data
	company_obj["description"] = company_experience_element.getElementsByTagName('description')[0].firstChild.data
	
	# Load Dates that the user worked for the company
	company_obj["started"] = {}
	company_obj["started"]["year"] = company_experience_element.getElementsByTagName('started')[0].getAttribute('year')
	company_obj["started"]["month"] = company_experience_element.getElementsByTagName('started')[0].getAttribute('month')

	company_obj["ended"] = {}
	try:
		company_obj["ended"]["year"] = company_experience_element.getElementsByTagName('ended')[0].getAttribute('year')
		company_obj["ended"]["month"] = company_experience_element.getElementsByTagName('ended')[0].getAttribute('month')
	except:
		company_obj["ended"] = None

	# Load Projects from this Company
	company_obj["projects"] = []
	for company_project_element in dom_root_element.getElementsByTagName('projects')[0].getElementsByTagName('project'):
		project_obj = {}
		project_obj["name"] = company_project_element.getElementsByTagName('name')[0].firstChild.data
		project_obj["url"] = company_project_element.getElementsByTagName('url')[0].firstChild.data
		project_obj["logo"] = company_project_element.getElementsByTagName('logo')[0].firstChild.data
		project_obj["description"] = company_project_element.getElementsByTagName('description')[0].firstChild.data
		
		project_obj["date"] = {}
		project_obj["date"]["year"] = company_project_element.getElementsByTagName('date')[0].getAttribute('year')
		project_obj["date"]["month"] = company_project_element.getElementsByTagName('date')[0].getAttribute('month')

		# Load Technologies that the user used in this project
		project_obj["technologies"] = []
		for company_tech_element in company_project_element.getElementsByTagName('technologies')[0].getElementsByTagName('tech'):
			project_obj["technologies"].append(company_tech_element.firstChild.data)

		company_obj["projects"].append(project_obj)

	cv_experience.append(company_obj)

# Load Freelance Experience
for company_experience_element in dom_root_element.getElementsByTagName('experience')[0].getElementsByTagName('freelance'):
	project_obj = {}
	project_obj["type"] = "freelance"
	project_obj["name"] = company_experience_element.getElementsByTagName('name')[0].firstChild.data
	project_obj["url"] = company_experience_element.getElementsByTagName('url')[0].firstChild.data
	project_obj["logo"] = company_experience_element.getElementsByTagName('logo')[0].firstChild.data
	project_obj["description"] = company_experience_element.getElementsByTagName('description')[0].firstChild.data

	project_obj["date"] = {}
	project_obj["date"]["year"] = company_experience_element.getElementsByTagName('date')[0].getAttribute('year')
	project_obj["date"]["month"] = company_experience_element.getElementsByTagName('date')[0].getAttribute('month')

	# Load Technologies that the user used in this project
	project_obj["technologies"] = []
	for company_tech_element in company_experience_element.getElementsByTagName('technologies')[0].getElementsByTagName('tech'):
		project_obj["technologies"].append(company_tech_element.firstChild.data)

	cv_experience.append(project_obj)

# Parse Open Source Projects
cv_opensourceprojects = []
for opensource_element in dom_root_element.getElementsByTagName('opensourceprojects')[0].getElementsByTagName('project'):
	opensource_obj = {}
	opensource_obj["name"] = opensource_element.getElementsByTagName('name')[0].firstChild.data
	opensource_obj["logo"] = opensource_element.getElementsByTagName('logo')[0].firstChild.data
	opensource_obj["description"] = opensource_element.getElementsByTagName('description')[0].firstChild.data
	opensource_obj["url"] = opensource_element.getElementsByTagName('url')[0].firstChild.data

	# Loop the Technologies used in Project
	opensource_obj["technologies"] = []
	for tech_element in opensource_element.getElementsByTagName('technologies')[0].getElementsByTagName('tech'):
		opensource_obj["technologies"].append(tech_element.firstChild.data)

	cv_opensourceprojects.append(opensource_obj)

"""
Ok damn! Everthing is loaded now. Now we assemble the CV
"""

# Open template so we can populate
read_file_handler = open(os.path.join('assets', 'template.html'))
template_page = read_file_handler.read() # Read in the Template
read_file_handler.close()

# Read in all the blocks
read_file_handler = open(os.path.join(os.path.join('assets', 'fragments'), 'experience.html'))
template_block_experience = read_file_handler.read() # Read in the Template
read_file_handler.close()

read_file_handler = open(os.path.join(os.path.join('assets', 'fragments'), 'experience_project.html'))
template_block_experience_project = read_file_handler.read() # Read in the Template
read_file_handler.close()

read_file_handler = open(os.path.join(os.path.join('assets', 'fragments'), 'education.html'))
template_block_education = read_file_handler.read() # Read in the Template
read_file_handler.close()

read_file_handler = open(os.path.join(os.path.join('assets', 'fragments'), 'project.html'))
template_block_project = read_file_handler.read() # Read in the Template
read_file_handler.close()

read_file_handler = open(os.path.join(os.path.join('assets', 'fragments'), 'opensourceproject.html'))
template_block_opensource_project = read_file_handler.read() # Read in the Template
read_file_handler.close()

# Add Personal Details
template_page = template_page.replace('{name}', cv_name)
template_page = template_page.replace('{email}', cv_email)
template_page = template_page.replace('{highscoolname}', cv_school_name)
template_page = template_page.replace('{highschoolyear}', cv_school_year)
template_page = template_page.replace('{distinctions}', " and ".join(cv_distinctions))

todays_date = date.today()
template_page = template_page.replace('{date}', todays_date.strftime("%A %d. %B %Y"))

# Replace the {profile} section with my letter
template_page = template_page.replace('{profile}', cv_cover_letter)

# Create the Skillset Block
skillblock = ""
skillobj = ""
count = 0

for skill in cv_skills:
	count = count + 1

	skillobj = skillobj + "<td>" + skill["name"] + "</td>"

	if skill["rating"] == "1":
		skillobj = skillobj + '<td><ul class="rating"><li><a class="activerating" href="#">1</a></li><li><a href="#">2</a></li><li><a href="#">3</a></li><li><a href="#">4</a></li><li><a href="#">5</a></li></ul></td>'
	elif skill["rating"] == "2":
		skillobj = skillobj + '<td><ul class="rating"><li><a href="#">1</a></li><li><a class="activerating" href="#">2</a></li><li><a href="#">3</a></li><li><a href="#">4</a></li><li><a href="#">5</a></li></ul></td>'
	elif skill["rating"] == "3":
		skillobj = skillobj + '<td><ul class="rating"><li><a href="#">1</a></li><li><a href="#">2</a></li><li><a class="activerating" href="#">3</a></li><li><a href="#">4</a></li><li><a href="#">5</a></li></ul></td>'
	elif skill["rating"] == "4":
		skillobj = skillobj + '<td><ul class="rating"><li><a href="#">1</a></li><li><a href="#">2</a></li><li><a href="#">3</a></li><li><a class="activerating" href="#">4</a></li><li><a href="#">5</a></li></ul></td>'
	elif skill["rating"] == "5":
		skillobj = skillobj + '<td><ul class="rating"><li><a href="#">1</a></li><li><a href="#">2</a></li><li><a href="#">3</a></li><li><a href="#">4</a></li><li><a class="activerating" href="#">5</a></li></ul></td>'

	if(count == 2):
		count = 0
		skillblock = skillblock + "<tr>" + skillobj + "</tr>"
		skillobj = ""

template_page = template_page.replace('{skillset}', skillblock)

# Was trying to see if this came out right. And it DID! :D
# print os.path.abspath(os.path.join(os.path.join('assets', 'template'), 'style.css'))

# Now we do Education
edu_block_str = ""
for edu in cv_education:

	edu_obj = template_block_education.replace('{name}', edu["name"])
	edu_obj = edu_obj.replace('{description}', edu["description"])
	edu_obj = edu_obj.replace('{datetime}', edu["timeframe"])

	if os.path.isfile(os.path.abspath(os.path.join(os.path.join('assets', 'custom'), edu["logo"]))):
		imagedata_uri = urllib.quote(open(os.path.abspath(os.path.join(os.path.join('assets', 'custom'), edu["logo"])), 'rb').read().encode('base64'))
		edu_obj = edu_obj.replace('{logo}', 'data:image/png;base64,' + str(imagedata_uri))
	else:
		imagedata_uri = urllib.quote(open(os.path.abspath(os.path.join(os.path.join('assets', 'custom'), 'default.png')), 'rb').read().encode('base64'))
		edu_obj = edu_obj.replace('{logo}', 'data:image/png;base64,' + str(imagedata_uri))

	edu_block_str = edu_block_str + edu_obj

template_page = template_page.replace('{education_block}', edu_block_str)

# And the Experience
exp_block_str = ""
for exp in cv_experience:

	if exp["type"] == 'company':
		# Do Company Stuff
		exp_obj = template_block_experience.replace('{name}', exp["name"])

		careerstarted = datetime.fromtimestamp(mktime(time.strptime("1 " + exp["started"]["month"] + " " + exp["started"]["year"], "%d %m %Y")))

		datetime_string = careerstarted.strftime("%B %Y")
		if exp["ended"] is None:
			datetime_string = datetime_string + " to <strong>Current</strong>"
		else:
			careerended = datetime.fromtimestamp(mktime(time.strptime("1 " + str(exp["ended"]["month"]) + " " + str(exp["ended"]["year"]), "%d %m %Y")))
			datetime_string = datetime_string + " to " + careerended.strftime("%B %Y")

		exp_obj = exp_obj.replace('{datetime}', datetime_string)

		if len(exp["projects"]) > 0:
			projectblock = """
			<div class="companyprojects">
			<div class="row" style="margin-bottom:5px;">
                <div class="span13 columns">
                    <h4>Projects while I worked for the company</h4>
                    <hr>
                </div>
            </div>
			"""
			try:
				for project in exp["projects"]:
					project_obj = template_block_experience_project.replace('{name}', project["name"])
					project_obj = project_obj.replace('{description}', project["description"])

					projectstarted = datetime.fromtimestamp(mktime(time.strptime("1 " + project["date"]["month"] + " " + project["date"]["year"], "%d %m %Y")))
					datetime_string = projectstarted.strftime("%B %Y")
					project_obj = project_obj.replace('{datetime}', datetime_string)

					# Loop Technologies used in project
					tech_obj = ''
					for tech in project["technologies"]:
						tech_obj = tech_obj + "<li>" + tech + "</li>"
					project_obj = project_obj.replace('{technologies}', tech_obj)

					# Load the Url if it exists
					try:
						project_obj = project_obj.replace('{url}', "<strong>" + project["url"] + "</strong> / ")
					except:
						project_obj = project_obj.replace('{url}', "")

					projectblock = projectblock + project_obj
				projectblock = projectblock + ""
			
			except:
				projectblock = ""
			exp_obj = exp_obj.replace('{projects}', projectblock)
		else:
			exp_obj = exp_obj.replace('{projects}', '')

	else:
		exp_obj = template_block_project.replace('{name}', exp["name"])
		exp_obj = exp_obj.replace('{description}', exp["description"])

		projectstarted = datetime.fromtimestamp(mktime(time.strptime("1 " + exp["date"]["month"] + " " + exp["date"]["year"], "%d %m %Y")))
		datetime_string = projectstarted.strftime("%B %Y")
		exp_obj = exp_obj.replace('{datetime}', datetime_string)

		# Loop Technologies used in project
		tech_obj = ""
		for tech in exp["technologies"]:
			tech_obj = tech_obj + "<li>" + tech + "</li>"
		exp_obj = exp_obj.replace('{technologies}', tech_obj)

		# Load the Url if it exists
		try:
			exp_obj = exp_obj.replace('{url}', "<strong>" + exp["url"] + "</strong> / ")
		except:
			exp_obj = exp_obj.replace('{url}', "")

	if os.path.isfile(os.path.abspath(os.path.join(os.path.join('assets', 'custom'), exp["logo"]))):
		imagedata_uri = urllib.quote(open(os.path.abspath(os.path.join(os.path.join('assets', 'custom'), exp["logo"])), 'rb').read().encode('base64'))
		exp_obj = exp_obj.replace('{logo}', 'data:image/png;base64,' + str(imagedata_uri))
	else:
		imagedata_uri = urllib.quote(open(os.path.abspath(os.path.join(os.path.join('assets', 'custom'), 'default.png')), 'rb').read().encode('base64'))
		exp_obj = exp_obj.replace('{logo}', 'data:image/png;base64,' + str(imagedata_uri))

	exp_obj = exp_obj.replace('{description}', exp["description"])
	exp_block_str = exp_block_str + exp_obj

template_page = template_page.replace('{experience_block}', exp_block_str)


opensource_block_str = ""
for op in cv_opensourceprojects:
	op_obj = template_block_opensource_project.replace('{name}', op["name"])
	op_obj = op_obj.replace('{description}', op["description"])
	op_obj = op_obj.replace('{url}', op["url"])

	# Loop Technologies used in project
	tech_obj = ""
	for tech in op["technologies"]:
		tech_obj = tech_obj + "<li>" + tech + "</li>"
	op_obj = op_obj.replace('{technologies}', tech_obj)

	# Load the Url if it exists
	try:
		op_obj = op_obj.replace('{url}', "<strong>" + op["url"] + "</strong> / ")
	except:
		op_obj = op_obj.replace('{url}', "")

	if os.path.isfile(os.path.abspath(os.path.join(os.path.join('assets', 'custom'), op["logo"]))):
		imagedata_uri = urllib.quote(open(os.path.abspath(os.path.join(os.path.join('assets', 'custom'), op["logo"])), 'rb').read().encode('base64'))
		op_obj = op_obj.replace('{logo}', 'data:image/png;base64,' + str(imagedata_uri))
	else:
		imagedata_uri = urllib.quote(open(os.path.abspath(os.path.join(os.path.join('assets', 'custom'), 'default.png')), 'rb').read().encode('base64'))
		op_obj = op_obj.replace('{logo}', 'data:image/png;base64,' + str(imagedata_uri))

	op_obj = op_obj.replace('{description}', op["description"])
	opensource_block_str = opensource_block_str + op_obj

template_page = template_page.replace('{opensource_block}', opensource_block_str)

# If the filename that the user gave us contains .html then we just save it as html else we save it as pdf
if ".html" in sys.argv[2] or ".htm" in sys.argv[2]:

	print("Generating CV in HTML format")

	# Write it out to the .HTML FILE
	write_file_handler = open(os.path.abspath(sys.argv[2]), 'w')
	write_file_handler.write(template_page)
	write_file_handler.close()

	print("Generated CV at " + os.path.abspath(sys.argv[2]))
elif ".doc" in sys.argv[2] or ".docx" in sys.argv[2]:
	# TODO generate the CV in word format
	pass
else:
	# We generate a PDF with the name they gave us
	pdf_filename = sys.argv[2]
	if ".pdf" not in pdf_filename:
		# Check if the output file has .pdf in the path if not we add it.
		pdf_filename = pdf_filename + ".pdf"

	print("Generating CV in PDF format")

	app = QApplication(sys.argv)

	try:
		if sys.frozen:
			plugin_path = os.path.join(constants.asset_dir, "qtplugins")
			self._application.addLibraryPath(plugin_path)
	except AttributeError:
		pass

	web = QWebView()

	printer = QPrinter()
	printer.setPageSize(QPrinter.A4)
	printer.setOutputFormat(QPrinter.PdfFormat)
	printer.setFullPage(True)
	printer.setOutputFileName(os.path.abspath(pdf_filename))

	def convertIt():
		web.print_(printer)
		print("Generated CV at " + os.path.abspath(pdf_filename))
		sys.exit(0)

	QObject.connect(web, SIGNAL("loadFinished(bool)"), convertIt)
	web.setHtml(template_page)

	sys.exit(app.exec_())
