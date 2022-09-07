import mysql.connector as mysql
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, QTableWidgetItem, QTableWidget, QWidget
from PyQt5.QtGui import QIcon, QPixmap

#connection = mysql.connect(user=sensitive_data, password=sensitive_data, host=sensitive_data)
cursor = connection.cursor()
license_bool = 0

class User:
	def __init__(self, id_user, id_role, login, password, name, last_name, email, license_key):
		self.id_user = id_user
		self.id_role = id_role
		self.login = login
		self.password = password
		self.name = name
		self.last_name = last_name
		self.email = email
		self.licesne_key = license_key

class MainWindow(QDialog):
	def __init__(self):
		super(MainWindow, self).__init__()
		loadUi("Login.ui", self)
		self.LoginButton.clicked.connect(self.connection)
		self.LicenseButton.clicked.connect(self.license_button)
		self.CreateAccountButton.clicked.connect(self.create_account)

		self.PasswordEdit.setEchoMode(QtWidgets.QLineEdit.Password)

	def connection(self):
		login = self.LoginEdit.text()
		password = self.PasswordEdit.text()
		global license_bool, user
		set_msg = 0
		database_matrix = []
		cursor.execute('Select * from fd46507.Uzytkownik')
		for n in cursor:
			database_matrix.append(n)
		for n in range(len(database_matrix)):
			if database_matrix[n][2] == login:
				if database_matrix[n][3] == password:
					if int(database_matrix[n][7]) != 0 or license_bool != 0:
						user = User(database_matrix[n][0], database_matrix[n][1], database_matrix[n][2], database_matrix[n][3], database_matrix[n][4], database_matrix[n][5], database_matrix[n][6], 1)
						screen2.MessageLabel.setText("Witaj {name} {last_name}!".format(name = user.name, last_name = user.last_name))
						widget.setCurrentIndex(2)
						if license_bool == 1:
							license_bool = 0
							if database_matrix[n][7] != 1:
								Id_name = int(database_matrix[n][0])
								cursor.execute('UPDATE fd46507.Uzytkownik SET License_key = 1 WHERE Id = {Id_name};'.format(Id_name = Id_name))
								connection.commit();
					else:
						set_msg = 1
		else:
			if set_msg == 1:
				self.MessageLabel.setText("Brak klucza licencyjnego")
			else:
				self.MessageLabel.setText("Błędne hasło lub login")
		self.LoginEdit.setText("")
		self.PasswordEdit.setText("")
		database_matrix.clear()

	def license_button(self):
		widget.setCurrentIndex(1)

	def create_account(self):
		widget.setCurrentIndex(3)

class License_key(QDialog):
	def __init__(self):
		super(License_key, self).__init__()
		loadUi("License_key.ui", self)
		self.ZatwierdzButton.clicked.connect(self.connection)

	def connection(self):
		license_key = self.lineEdit.text()
		license = []
		global license_bool
		cursor.execute('Select * from fd46507.Klucze_licencyjne')
		for n in cursor:
			word = str(n)
			license.append(word[2:-3])
		if license_key in license:
			widget.setCurrentIndex(widget.currentIndex()-1)
			license_bool = 1
			mainwindow.MessageLabel.setText("Wprowadzono prawidłowy klucz")
		else:
			widget.setCurrentIndex(widget.currentIndex()-1)
			mainwindow.MessageLabel.setText("Wprowadzono błędny klucz")
		license_key = self.lineEdit.setText("")
		license.clear()

class Screen2(QDialog):
	def __init__(self):
		global user
		super(Screen2, self).__init__()
		loadUi("Screen2.ui", self)
		self.WylogujButton.clicked.connect(self.logout)
		self.KursPodstawowyButton.clicked.connect(self.basic_course)
		self.ProfilButton.clicked.connect(self.profil)
		
	def logout(self):
		widget.setCurrentIndex(0)
		mainwindow.MessageLabel.setText("Wylogowano z systemu")

	def basic_course(self):
		widget.setCurrentIndex(4)

	def profil(self):
		profil.NameLabel.setText(str(user.name))
		profil.LastNameLabel.setText(str(user.last_name))
		profil.EmailLabel.setText(str(user.email))
		widget.setCurrentIndex(9)


class Create_Account(QDialog):
	def __init__(self):
		global user
		super(Create_Account, self).__init__()
		loadUi("CreateAccount.ui", self)
		self.CreateAccountButton.clicked.connect(self.create_account)
		self.BackButton.clicked.connect(self.back)
		self.PasswordEdit.setEchoMode(QtWidgets.QLineEdit.Password)

	def create_account(self):
		login = self.LoginEdit.text()
		password = self.PasswordEdit.text()
		name = self.NameEdit.text()
		last_name = self.LastNameEdit.text()
		email = self.EmailEdit.text()

		if (len(login) == 0 or " " in login) or (len(password) == 0 or " " in password) or (len(name) == 0 or " " in name) or (len(last_name) == 0 or " " in last_name) or (len(email) == 0 or " " in email):
			mainwindow.MessageLabel.setText("Nie można używać takich znaków!")
			widget.setCurrentIndex(0)
			self.LoginEdit.setText("")
			self.PasswordEdit.setText("")
			self.NameEdit.setText("")
			self.LastNameEdit.setText("")
			self.EmailEdit.setText("")
			return

		if len(password) < 6:
			mainwindow.MessageLabel.setText("Hasło jest zbyt krótkie!")
			widget.setCurrentIndex(0)
			self.LoginEdit.setText("")
			self.PasswordEdit.setText("")
			self.NameEdit.setText("")
			self.LastNameEdit.setText("")
			self.EmailEdit.setText("")
			return

		cursor.execute('SELECT Login FROM fd46507.Uzytkownik;')
		for n in cursor:
			if login == n[0]:
				mainwindow.MessageLabel.setText("Taki login już istnieje!")
				widget.setCurrentIndex(0)
				self.LoginEdit.setText("")
				self.PasswordEdit.setText("")
				self.NameEdit.setText("")
				self.LastNameEdit.setText("")
				self.EmailEdit.setText("")
				return

		cursor.execute('SELECT Id FROM fd46507.Uzytkownik order by 1 desc limit 1;')
		for n in cursor:
			last_id = (int(str(n)[1]))
		last_id += 1
		last_id = str(last_id)

		cursor.execute('Insert into fd46507.Uzytkownik values("{last_id_}", "0", "{login_}", "{password_}", "{name_}", "{last_name_}", "{email_}", "0");'.format(last_id_ = str(last_id), login_ = str(login), password_ = str(password), name_ = str(name), last_name_ = str(last_name), email_ = str(email)))
		connection.commit();
		mainwindow.MessageLabel.setText("Twoje konto zostało poprawnie założone!")
		self.LoginEdit.setText("")
		self.PasswordEdit.setText("")
		self.NameEdit.setText("")
		self.LastNameEdit.setText("")
		self.EmailEdit.setText("")
		widget.setCurrentIndex(0)

	def back(self):
		self.LoginEdit.setText("")
		self.PasswordEdit.setText("")
		self.NameEdit.setText("")
		self.LastNameEdit.setText("")
		self.EmailEdit.setText("")
		widget.setCurrentIndex(0)

class Chapters(QDialog):
	def __init__(self):
		global user
		super(Chapters, self).__init__()
		loadUi("Chapters.ui", self)
		self.BackButton.clicked.connect(self.back)
		self.CountriesButton.clicked.connect(self.countries)

	def back(self):
		widget.setCurrentIndex(2)

	def countries(self):
		widget.setCurrentIndex(5)

class Countries(QDialog):
	def __init__(self):
		global user
		super(Countries, self).__init__()
		loadUi("Countries.ui", self)
		self.BackButton.clicked.connect(self.back)
		self.EuropeButton.clicked.connect(self.europe_presentation)
		self.TestEuropeButton.clicked.connect(self.europe_test)

	def back(self):
		widget.setCurrentIndex(4)

	def europe_presentation(self):
		widget.setCurrentIndex(6)

	def europe_test(self):
		testy = []
		cursor.execute('SELECT * FROM fd46507.Oceny where ID = {id};'.format(id = user.id_user))
		for n in cursor:
			testy.append(n)
		for n in range(len(testy)):
			if testy[n][5] == 1:
				results.PointLabel.setText(str(testy[n][1]))
				results.MaxPointLabel.setText(str(testy[n][2]))
				results.PercentLabel.setText(str(testy[n][4]))
				results.GradeLabel.setText(str(testy[n][3]))
				test.AlreadyDone = 1
				widget.setCurrentIndex(8)
				testy.clear()
				return
			else:
				test.AlreadyDone = 0
				testy.clear()
		f = open('EuropeQuestions.txt','r',encoding='utf-8')
		line = f.readline()
		lista = []
		while line != '':
			lista.append(line.replace('\n', ''))
			line = f.readline()
		f.close()

		test.TestId = 1
		test.QuestionLabel.setText(lista[0])
		test.Answer1Label.setText(lista[1])
		test.Answer2Label.setText(lista[2])
		test.Answer3Label.setText(lista[3])
		test.Answer4Label.setText(lista[4])
		widget.setCurrentIndex(7)
		lista.clear()

class EuropeanCountries(QDialog):
	def __init__(self):
		global user
		super(EuropeanCountries, self).__init__()
		loadUi("EuropeanCountries.ui", self)
		self.PhotoId = 1
		self.QuitButton.clicked.connect(self.quit)
		self.NextButton.clicked.connect(self.next)
		self.BackButton.clicked.connect(self.back)

	def quit(self):
		widget.setCurrentIndex(5)
		pixmap = QPixmap("assets/Chapters/Topics/Panstwa/PanstwaEuropy/1.jpg")
		self.PhotoLabel.setPixmap(pixmap)
		self.PhotoId = 1

	def back(self):
		if self.PhotoId == 1:
			return
		else:
			self.PhotoId -= 1
			pixmap = QPixmap("assets/Chapters/Topics/Panstwa/PanstwaEuropy/{next}.jpg".format(next = self.PhotoId))
			self.PhotoLabel.setPixmap(pixmap)

	def next(self):
		if self.PhotoId < 27:
			self.PhotoId += 1
			pixmap = QPixmap("assets/Chapters/Topics/Panstwa/PanstwaEuropy/{next}.jpg".format(next = self.PhotoId))
			self.PhotoLabel.setPixmap(pixmap)

class Test(QDialog):
	def __init__(self):
		global user
		super(Test, self).__init__()
		loadUi("Test.ui", self)
		self.Points = 0
		self.CurrentIndex = 5
		self.TestId = 0
		self.AlreadyDone = 0
		self.Answered = 0
		self.QuitTestButton.clicked.connect(self.quit_test)
		self.NextButton.clicked.connect(self.next)
		self.Answer1Button.clicked.connect(self.answer1)
		self.Answer2Button.clicked.connect(self.answer2)
		self.Answer3Button.clicked.connect(self.answer3)
		self.Answer4Button.clicked.connect(self.answer4)

		f = open('EuropeQuestions.txt','r',encoding='utf-8')
		line = f.readline()
		self.lista = []
		while line != '':
			self.lista.append(line.replace('\n', ''))
			line = f.readline()
		f.close()

	def quit_test(self):
		results.PointLabel.setText(str(self.Points))
		results.MaxPointLabel.setText(str(int(len(self.lista)/6)))
		perc_word = str(round((self.Points/(len(self.lista)/6)) * 100, 2))
		perc_word += " %"
		grade = "0"
		results.PercentLabel.setText(perc_word)
		if (self.Points/(len(self.lista)/6)) * 100 < 25:
			results.GradeLabel.setText("1")
			grade = "1"
		elif 25 <= (self.Points/(len(self.lista)/6)) * 100 < 30:
			results.GradeLabel.setText("1+")
			grade = "1+"
		elif 30 <= (self.Points/(len(self.lista)/6)) * 100 < 35:
			results.GradeLabel.setText("2-")
			grade = "2-"
		elif 35 <= (self.Points/(len(self.lista)/6)) * 100 < 45:
			results.GradeLabel.setText("2")
			grade = "2"
		elif 45 <= (self.Points/(len(self.lista)/6)) * 100 < 50:
			results.GradeLabel.setText("2+")
			grade = "2+"
		elif 50 <= (self.Points/(len(self.lista)/6)) * 100 < 55:
			results.GradeLabel.setText("3-")
			grade = "3-"
		elif 55 <= (self.Points/(len(self.lista)/6)) * 100 < 70:
			results.GradeLabel.setText("3")
			grade = "3"
		elif 70 <= (self.Points/(len(self.lista)/6)) * 100 < 75:
			results.GradeLabel.setText("3+")
			grade = "3+"
		elif 75 <= (self.Points/(len(self.lista)/6)) * 100 < 80:
			results.GradeLabel.setText("4-")
			grade = "4-"
		elif 80 <= (self.Points/(len(self.lista)/6)) * 100 < 85:
			results.GradeLabel.setText("4")
			grade = "4"
		elif 85 <= (self.Points/(len(self.lista)/6)) * 100 < 87:
			results.GradeLabel.setText("4+")
			grade = "4+"
		elif 87 <= (self.Points/(len(self.lista)/6)) * 100 < 90:
			results.GradeLabel.setText("5-")
			grade = "5-"
		elif 90 <= (self.Points/(len(self.lista)/6)) * 100 < 95:
			results.GradeLabel.setText("5")
			grade = "5"
		elif 95 <= (self.Points/(len(self.lista)/6)) * 100 < 97:
			results.GradeLabel.setText("5+")
			grade = "5+"
		elif 98 <= (self.Points/(len(self.lista)/6)) * 100 < 99:
			results.GradeLabel.setText("6-")
			grade = "6-"
		else:
			results.GradeLabel.setText("6")
			grade = "6"

		if self.AlreadyDone != 1:
			cursor.execute('Insert into fd46507.Oceny values("{Id}", {Points}, {Max}, "{Grade}", {Percent}, {Id_test}, "Państwa Europy");'.format(Id = user.id_user, Points = self.Points, Max = int(len(self.lista)/6), Grade = grade, Percent = round((self.Points/(len(self.lista)/6)) * 100, 2), Id_test = self.TestId))
			connection.commit();
		self.lista.clear()
		widget.setCurrentIndex(8)

	def next(self):
		if self.CurrentIndex < (len(self.lista) - 1):
			self.Answer1Label.setStyleSheet("background-color: rgb(222, 222, 222);")
			self.Answer2Label.setStyleSheet("background-color: rgb(222, 222, 222);")
			self.Answer3Label.setStyleSheet("background-color: rgb(222, 222, 222);")
			self.Answer4Label.setStyleSheet("background-color: rgb(222, 222, 222);")
			self.QuestionLabel.setText(self.lista[self.CurrentIndex+1])
			self.Answer1Label.setText(self.lista[self.CurrentIndex+2])
			self.Answer2Label.setText(self.lista[self.CurrentIndex+3])
			self.Answer3Label.setText(self.lista[self.CurrentIndex+4])
			self.Answer4Label.setText(self.lista[self.CurrentIndex+5])
			self.CurrentIndex += 6
			self.Answered = 0
		else:
			self.quit_test()

	def answer1(self):
		if self.Answered != 1:
			if self.lista[self.CurrentIndex] == "1":
				self.Answer1Label.setStyleSheet("background-color: rgb(0, 255, 0);")
				self.Points += 1
				self.Answered = 1
			else:
				self.Answer1Label.setStyleSheet("background-color: rgb(255, 0, 0);")
				self.Answered = 1

	def answer2(self):
		if self.Answered != 1:
			if self.lista[self.CurrentIndex] == "2":
				self.Answer2Label.setStyleSheet("background-color: rgb(0, 255, 0);")
				self.Points += 1
				self.Answered = 1
			else:
				self.Answer2Label.setStyleSheet("background-color: rgb(255, 0, 0);")
				self.Answered = 1

	def answer3(self):
		if self.Answered != 1:
			if self.lista[self.CurrentIndex] == "3":
				self.Answer3Label.setStyleSheet("background-color: rgb(0, 255, 0);")
				self.Points += 1
				self.Answered = 1
			else:
				self.Answer3Label.setStyleSheet("background-color: rgb(255, 0, 0);")
				self.Answered = 1

	def answer4(self):
		if self.Answered != 1:
			if self.lista[self.CurrentIndex] == "4":
				self.Answer4Label.setStyleSheet("background-color: rgb(0, 255, 0);")
				self.Points += 1
				self.Answered = 1
			else:
				self.Answer4Label.setStyleSheet("background-color: rgb(255, 0, 0);")
				self.Answered = 1

class Results(QDialog):
	def __init__(self):
		global user
		super(Results, self).__init__()
		loadUi("Results.ui", self)
		self.QuitTestButton.clicked.connect(self.quit)

	def quit(self):
		widget.setCurrentIndex(5)

class Profil(QDialog):
	def __init__(self):
		global user
		super(Profil, self).__init__()
		loadUi("Profil.ui", self)
		self.BackButton.clicked.connect(self.back)
		self.GradesButton.clicked.connect(self.grades)
		self.ChangePasswordButton.clicked.connect(self.change_passwd)

	def change_passwd(self):
		widget.setCurrentIndex(11)

	def back(self):
		widget.setCurrentIndex(2)

	def grades(self):
		grades_list = []
		cursor.execute('Select * from fd46507.Oceny where ID = "{id}"'.format(id = user.id_user))
		for n in cursor:
			grades_list.append(n)
		grades.tableWidget.setRowCount(len(grades_list))
		for i in range(len(grades_list)):
				grades.tableWidget.setItem(i, 0, QTableWidgetItem(str(grades_list[i][3])))
				grades.tableWidget.setItem(i, 1, QTableWidgetItem(str(grades_list[i][1])))
				grades.tableWidget.setItem(i, 2, QTableWidgetItem(str(grades_list[i][2])))
				grades.tableWidget.setItem(i, 3, QTableWidgetItem(str(grades_list[i][4])))
				grades.tableWidget.setItem(i, 4, QTableWidgetItem(str(grades_list[i][6])))
		grades_list.clear()
		widget.setCurrentIndex(10)

class Grades(QDialog):
	def __init__(self):
		global user
		super(Grades, self).__init__()
		loadUi("Grades.ui", self)
		self.BackButton.clicked.connect(self.back)

	def back(self):
		widget.setCurrentIndex(9)

class ChangePassword(QDialog):
	def __init__(self):
		global user
		super(ChangePassword, self).__init__()
		loadUi("ChangePassword.ui", self)
		self.ZatwierdzButton.clicked.connect(self.accept)
		self.BackButton.clicked.connect(self.back)
		self.PasswordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
		self.Password2Edit.setEchoMode(QtWidgets.QLineEdit.Password)
		self.NewPasswordEdit.setEchoMode(QtWidgets.QLineEdit.Password)

	def back(self):
		self.InfoLabel.setText("")
		widget.setCurrentIndex(9)

	def accept(self):
		login = self.LoginEdit.text()
		password = self.PasswordEdit.text()
		password2 = self.Password2Edit.text()
		new_password = self.NewPasswordEdit.text()
		database_matrix = []
		cursor.execute('Select * from fd46507.Uzytkownik')
		for n in cursor:
			database_matrix.append(n)
		for n in range(len(database_matrix)):
			if database_matrix[n][2] == login and user.login == login:
				if database_matrix[n][3] == password and new_password == password2 and user.password == password:
					cursor.execute('UPDATE fd46507.Uzytkownik SET Haslo = "{passwd}" WHERE ID = {id};'.format(passwd = new_password, id = user.id_user))
					connection.commit();
					self.LoginEdit.setText("")
					self.PasswordEdit.setText("")
					self.Password2Edit.setText("")
					self.NewPasswordEdit.setText("")
					self.InfoLabel.setText("Hasło zostało zmienione!")
					database_matrix.clear()
					return
		self.InfoLabel.setText("Błędne hasło lub login!")
		database_matrix.clear()

user = User(0,0,0,0,0,0,0,0)
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

mainwindow = MainWindow() #0
licensekey = License_key() #1
screen2 = Screen2() #2
createaccount = Create_Account() #3
chapters = Chapters() #4
countries = Countries() #5
europeancountries = EuropeanCountries() #6
test = Test() #7
results = Results() #8
profil = Profil() #9
grades = Grades() #10
changepassword = ChangePassword() #11

widget.addWidget(mainwindow)
widget.addWidget(licensekey)
widget.addWidget(screen2)
widget.addWidget(createaccount)
widget.addWidget(chapters)
widget.addWidget(countries)
widget.addWidget(europeancountries)
widget.addWidget(test)
widget.addWidget(results)
widget.addWidget(profil)
widget.addWidget(grades)
widget.addWidget(changepassword)

widget.setFixedWidth(800)
widget.setFixedHeight(600)
widget.show()

try:
	sys.exit(app.exec_())
except:
	print("")