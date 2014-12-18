#!/usr/bin/python
'''
A Python program for managing information about
courses and students at archaeological excavations
'''
from easygui import *
import sqlite3
import pprint, os

TITLE = "Course Register"
DATABASE_FILE = "registration.db"
debugging  = False
cursor     = None # a global
courseId   = None # a global
courseName = None # a global
studentId  = None # a global
sep = "."

"""
Assumptions:

there are two tables, with primary keys indicated by an asterisk:

	courses(courseId*, courseName)
	students(courseId*,studentId*,studentName,studentName)

and a foreign key to enforce id-dependency:
	foreign key fk_courseId (courseId) in table students references table courses
"""

#-----------------------------------------------------------------------
#          reportResults
#-----------------------------------------------------------------------
def format(courseId,studentId):
	return "%s%s%s" % (courseId,sep,studentId)

#-----------------------------------------------------------------------
#          reportResults
#-----------------------------------------------------------------------
def reportResults(resultsSet,msg=""):
	if not debugging: return
	if msg: print msg,
	print "fetched ", len(resultsSet), "rows"
	pprint.pprint(resultsSet)
	print


#-----------------------------------------------------------------------
#          createCourse
#-----------------------------------------------------------------------
def createCourse():
	global connection, cursor, courseId, studentId

	msg = "Enter data about the new course"
	fieldNames = ["Course ID", "Course Name"]
	fieldValues = []

	while True:
		fieldValues = multenterbox(msg,TITLE, fieldNames, fieldValues)
		if fieldValues == None: return

		# make sure that none of the fields was left blank
		errors = 0
		for i in range(len(fieldNames)):
			if fieldValues[i].strip() == "":
				msgbox('"%s" is a required field.' % fieldNames[i])
				errors += 1
				break
		if errors > 0: continue

		newCourseId = fieldValues[0]
		newCourseId = "".join(newCourseId.split())  # remove all whitespace

		if existsCourse(newCourseId):
			msgbox("Course " + newCourseId + " already exists.", "Error")
			continue
		else:
			break


	newCourseId, courseName = fieldValues
	cursor.execute(
	  'INSERT INTO courses '
	  '(courseId, courseName) '
	  'VALUES (?, ?)',
	  (newCourseId, courseName)
	  )
	connection.commit()
	courseId = newCourseId  # reset the global variable

	msg = "Course " + courseId + " (" + courseName + ") was created."
	msgbox(msg,TITLE)

#-----------------------------------------------------------------------
#          displayCourses
#-----------------------------------------------------------------------
def displayCourses():
	listOfCourses= getListOfCoursesAndCourseNames()
	if not listOfCourses:
		msgbox("There are no courses in the courses database table.")
		return

	listOfCourses = ["  ".join(course) for course in listOfCourses]
	courses = "\n".join(listOfCourses) # convert the list to a string
	textbox("Here is a list of the courses", TITLE, courses)


#-----------------------------------------------------------------------
#          selectCourse
#-----------------------------------------------------------------------
def selectCourse():
	global courseId, courseName
	listOfCourses= getListOfCoursesAndCourseNames()
	if not listOfCourses:
		msgbox("There are no courses in the courses database table.")
		return

	choices = [ str(x[0]) + "  " + str(x[1]) for x in listOfCourses]
	msg = "Select a course"
	choice = choicebox(msg,TITLE,choices)
	courseId, courseName = choice.split(None,1)


#-----------------------------------------------------------------------
#          getListOfCourses
#-----------------------------------------------------------------------
def getListOfCourses():
	global connection, cursor
	listOfCourses=[]
	cursor.execute('SELECT courseId FROM courses ORDER BY courseId ASC')
	resultsSet = cursor.fetchall()

	if len(resultsSet) == 0: return None
	reportResults(resultsSet,"getListOfCourses")

	listOfCourses = [str(row[0]) for row in resultsSet]
	return listOfCourses

#-----------------------------------------------------------------------
#          getListOfCoursesAndCourseNames
#-----------------------------------------------------------------------
def getListOfCoursesAndCourseNames():
	global connection, cursor
	listOfCourses=[]
	cursor.execute('SELECT courseId, courseName FROM courses ORDER BY courseId ASC')
	resultsSet = cursor.fetchall()

	if len(resultsSet) == 0: return None
	reportResults(resultsSet,"getListOfCoursesAndCourseNames")

	listOfCourses = [[str(row[0]),str(row[1])] for row in resultsSet]
	return listOfCourses

#-----------------------------------------------------------------------
#          createStudent
#-----------------------------------------------------------------------
def createStudent():
	global connection, cursor, courseId

	while True:
		studentId = enterbox("Enter the student Id for the new student")
		if not studentId: return
		if existsStudent(courseId,studentId):
			msgbox("Student " + courseId + sep + studentId + " already exists.", "Error")
		else:
			break

	msg = "Enter the attributes of the new student"
	fieldNames = ["Student Name", "Student Phone"]
	fieldValues = []

	while True:
		fieldValues = multenterbox(msg,TITLE, fieldNames, fieldValues)
		if fieldValues == None: return

		# make sure that none of the fields was left blank
		errors = 0
		for i in range(len(fieldNames)):
				if fieldValues[i].strip() == "":
					msgbox('"%s" is a required field.' % fieldNames[i])
					errors += 1
					break
		if errors == 0: break

	studentName, studentPhone = fieldValues
	cursor.execute(
	  'INSERT INTO students '
	  '(courseId, studentId, studentName, studentPhone) '
	  'VALUES (?, ?, ?, ?)',
	  (courseId, studentId, studentName, studentPhone)
	  )
	connection.commit()

	msg = "Student " + courseId + sep + studentId + " was created.\n\n"
	msg += "studentName = " + studentName + "\n"
	msg += "studentPhone = " + studentPhone
	msgbox(msg,TITLE)


#-----------------------------------------------------------------------
#          deleteCourse
#-----------------------------------------------------------------------
def deleteCourse():
	global connection, cursor, courseId, studentId

	cursor.execute(
	'DELETE FROM students '
	'WHERE courseId = ? ',
	(courseId,)
	)

	cursor.execute(
	'DELETE FROM courses '
	'WHERE courseId = ? ',
	(courseId,)
	)

	connection.commit()
	msgbox("Course " +courseId + " (and all of its students) was deleted.",TITLE)
	courseId = None
	studentId = None


#-----------------------------------------------------------------------
#          deleteStudent
#-----------------------------------------------------------------------
def deleteStudent():
	global connection, cursor, courseId, studentId
	cursor.execute(
	  'DELETE FROM students '
	  'WHERE courseId = ? and studentId = ? ',
	  (courseId, studentId)
	  )

	connection.commit()
	msgbox("Student " + format(courseId,studentId) + " was deleted.",TITLE)
	studentId = None


#-----------------------------------------------------------------------
#          updateStudent
#-----------------------------------------------------------------------
def updateStudent():
	global connection, cursor, courseId
	msgbox("This function is not yet implemented.")


#-----------------------------------------------------------------------
#          existsCourse
#-----------------------------------------------------------------------
def existsCourse(courseId):
	global connection, cursor
	cursor.execute('SELECT courseId '
				   'from courses '
				   'WHERE courseId = ?', (courseId,))
	resultsSet = cursor.fetchall()
	if resultsSet: return True
	else:          return False


#-----------------------------------------------------------------------
#          existsStudent
#-----------------------------------------------------------------------
def existsStudent(courseId,studentId):
	global connection, cursor
	cursor.execute('SELECT courseId,studentId '
				   'FROM students '
				   'WHERE courseId = ? and studentId = ?', (courseId,studentId))
	resultsSet = cursor.fetchall()
	if resultsSet: return True
	else:          return False


#-----------------------------------------------------------------------
#          selectStudent
#-----------------------------------------------------------------------
def selectStudent():
	global connection, cursor, courseId, studentId

	resultsSet = getStudentsForCourse(courseId)
	if len(resultsSet) == 0:
		msgbox("There are no students for course " + courseId)
		return None

	choices = []
	for row in resultsSet:
		studentId, studentName, studentPhone = row
		choice = "%s | %s (%s)" %(studentId.ljust(10), studentName, studentPhone)
		choices.append(choice)

	choice = choicebox("Select the desired student for " + courseId, TITLE, choices)
	if not choice:
		return None
	words = choice.split()
	studentId = words[0]


#-----------------------------------------------------------------------
#          displayStudentsForCurrentCourse
#-----------------------------------------------------------------------
def displayStudentsForCurrentCourse():
	resultsSet = getStudentsForCourse(courseId)
	if len(resultsSet) == 0:
		msgbox("There are no students for course " + courseId )
		return None

	text = ""
	for row in resultsSet:
		studentId, studentName, studentPhone = row
		choice = "%s | %s (%s)\n" %(studentId.ljust(10), studentName, studentPhone)
		text += choice

	textbox("Here are the students for course " + courseId, TITLE, text)


#-----------------------------------------------------------------------
#          displayAllStudents
#-----------------------------------------------------------------------
def displayAllStudents():
	listOfCourses= getListOfCoursesAndCourseNames()
	if not listOfCourses:
		msgbox("There are no courses in the courses database table.")
		return

	text = []
	for courseInfo in listOfCourses:
		courseId, courseName = courseInfo
		text.append("")
		text.append("Course: %s (%s)" % (courseId,courseName))
		resultsSet = getStudentsForCourse(courseId)

		if len(resultsSet) == 0:
			text.append("    " + "(no students registered)")
		for row in resultsSet:
			#pprint.pprint(row)
			studentId, studentName, studentPhone = row
			studentInfo = "%s | %s (%s)" %(format(courseId,studentId).ljust(10), studentName, studentPhone)
			text.append("    " + studentInfo)


	textbox("Here are all of the students", TITLE, "\n".join(text))



#-----------------------------------------------------------------------
#          getStudentsForCourse
#-----------------------------------------------------------------------
def getStudentsForCourse(courseId):
	global connection, cursor

	if courseId:
		cursor.execute('SELECT studentId, studentName, studentPhone '
			'FROM students '
			'WHERE courseId = ?', (courseId,))
	else:
		cursor.execute('SELECT courseId, studentId, studentName, studentPhone '
			'FROM students '
		)
	resultsSet = cursor.fetchall()

	reportResults(resultsSet,"getStudentsForCourse " + str(courseId))
	return resultsSet


#-----------------------------------------------------------------------
#          main
#-----------------------------------------------------------------------
def main():
	global courseId, studentId, courseName
	while True:
		choices = \
			[ "CC - create a new course"
			, "CD - display a list of courses"
			, "CS - select a course"
			, "AD - display a list of all students in all courses"
			]

		if courseId:
			choices.extend(
			[ "SC - create a new student for course " + str(courseId)
			, "SS - select a student for course " + str(courseId)
			, "SD - display a list of existing students for course " + str(courseId)
			, "CX - delete course " + str(courseId)
			])

		if studentId:
			choices.extend(
			[ "SX - delete student " + format(courseId,studentId)
			, "SU - update student " + format(courseId,studentId)
			])

		msg = "Pick a function."
		msg += "\nCurrent course  is " + str(courseId) + " (" + str(courseName) + ")"
		msg += "\nCurrent student is " + str(studentId)

		choice = choicebox(msg, TITLE, choices)
		if not choice: return
		choiceId = choice.split()[0]  # get the first "word" of the choice

		if   choiceId == "CC": createCourse()
		elif choiceId == "CX": deleteCourse()
		elif choiceId == "CS": selectCourse()
		elif choiceId == "CD": displayCourses()
		elif choiceId == "SC": createStudent()
		elif choiceId == "SD": displayStudentsForCurrentCourse()
		elif choiceId == "SX": deleteStudent()
		elif choiceId == "AD": displayAllStudents()
		elif choiceId == "SU": updateStudent()
		elif choiceId == "SS": selectStudent()
		else:
			raise AssertionError("Program logic error:\n"
				"I do not recognize choice " + str(choice))


#-----------------------------------------------------------------------
#          createTables
#-----------------------------------------------------------------------
def createTables():
	global connection
	cursor = connection.cursor()

	cursor.execute('''create table courses
	( courseId text
	, courseName text
	)''')

	cursor.execute('''create table students
	( courseId     text
	, studentId    text
	, studentName  text
	, studentPhone text
	)''')
	connection.commit()
	cursor.close()
	msgbox("courses and students tables were created.",TITLE)

#-----------------------------------------------------------------------
#          start everything
#-----------------------------------------------------------------------
if __name__ == "__main__":
	print TITLE, "starts"
	if debugging:
		connection = sqlite3.connect(':memory:')
		createTables()
	else:
		if os.path.exists(DATABASE_FILE):
			connection = sqlite3.connect(DATABASE_FILE)
		else:
			connection = sqlite3.connect(DATABASE_FILE)
			createTables()

	cursor = connection.cursor()
	main()
	connection.close()
	print TITLE, "ends"
