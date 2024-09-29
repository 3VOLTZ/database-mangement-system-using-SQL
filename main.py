from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, \
     QVBoxLayout, QComboBox, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800,600)
        
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")
        
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)
        
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)
        
        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        edit_menu_item.addAction(search_action) 
        search_action.triggered.connect(self.search)
        
        
        # Add to toolbar as well if needed
        

        
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID","Name","Course","Contact"))
        self.table.verticalHeader().setVisible(False)    #to hide the extra index column
        self.setCentralWidget(self.table)
        
        #Create toolbar and toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)
    
        
        #Status Bar and Status elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        self.table.cellClicked.connect(self.cell_clicked)
        
        
    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)
        
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        delete_all_button = QPushButton("Delete All Records")  # Add Delete All Records button
        delete_all_button.clicked.connect(self.delete_all)      # Connect it to delete_all method
        
        # Remove previous buttons from the status bar
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        # Add new buttons to the status bar
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)
        self.statusbar.addWidget(delete_all_button)  # Add Delete All button to the status bar


    def delete_all(self):
        dialog = DeleteAllDialog()
        dialog.exec()

        
    

    
    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)     #to ensure no duplicate data
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.table
        connection.close()
        
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()
        
    def search(self):
        dialog = SearchDialog()
        dialog.exec()
    
    def edit(self):
        dialog = EditDialog()
        dialog.exec()
        
    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()
        
    def about(self):
        dialog = AboutDialog()
        dialog.exec()
        
class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """ A student Database Management System to store and modify student data  """ 
        self.setText(content)             

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        
        layout = QVBoxLayout()
        #get name from selected row
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()
        
        #get id from selected row
        self.student_id = main_window.table.item(index, 0).text()
        #Add student name
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        
        course_name = main_window.table.item(index, 2).text()
        #add courses
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)
        
        #Add contact
        mobile = main_window.table.item(index, 3).text()
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Contact")
        layout.addWidget(self.mobile)
        
        #Add Submit button
        button = QPushButton("Update")
        button.clicked.connect(self.update_Student)
        layout.addWidget(button)
        
        
        self.setLayout(layout)

class DeleteAllDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete All Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete all records?")
        yes = QPushButton("Yes")
        no = QPushButton("No")
        
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)
        
        yes.clicked.connect(self.delete_all_students)
        no.clicked.connect(self.close)

    def delete_all_students(self):
        # Connect to the database and delete all records
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE from students")  # Delete all rows
        connection.commit()
        cursor.close()
        connection.close()

        # Refresh the table data
        main_window.load_data()

        # Close the dialog
        self.close()

        # Show a confirmation message
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("All records have been successfully deleted.")
        confirmation_widget.exec()


    def update_Student(Self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                    (Self.student_name.text(), 
                     Self.course_name.itemText(Self.course_name.currentIndex()),
                     Self.mobile.text(), 
                     Self.student_id ))
        connection.commit()
        cursor.close()
        connection.close()
        
        #refresh table
        main_window.load_data()  
    
class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")
        
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)
        
        yes.clicked.connect(self.delete_student)
        
    def delete_student(Self):
        index = main_window.table.currentRow()
        #get id from selected row
        student_id = main_window.table.item(index, 0).text()
        
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?", (student_id, ))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data() 
        
        Self.close()
        
        confirmation_widget =  QMessageBox() 
        confirmation_widget.setWindowTitle("Success") 
        confirmation_widget.setText("The record was succesfully deleted")  
        confirmation_widget.exec()

class InsertDialog(QDialog):       #for dialog window that will display as pop up window
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        
        layout = QVBoxLayout()
        
        #Add student name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        
        #add courses
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)
        
        #Add contact
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Contact")
        layout.addWidget(self.mobile)
        
        #Add Submit button
        button = QPushButton("Submit")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)
        
        
        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        
class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Set window title and size
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Create layout and input widget
        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Create button
        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        rows = list(result)[0]
        print(rows)
        items = main_window.table.findItems("John Smith", Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())        