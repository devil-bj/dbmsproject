import pymysql

from Service.ServiceProvider import app

# Database connection parameters
host = 'localhost'
user = 'root'  # Replace with your MySQL username
password = 'American.1@#@'  # Replace with your MySQL password
db_name = 'university_db'  # Name of the database to create

# Connect to MySQL
connection = pymysql.connect(host=host, user=user, password=password)

try:
    with connection.cursor() as cursor:
        # Create a new database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")

        # Create table for Departments
        create_departments_table = """
        CREATE TABLE IF NOT EXISTS Departments (
            DepartmentID INT AUTO_INCREMENT ,
            DepartmentName VARCHAR(255) NOT NULL,
            DepartmentCode VARCHAR(4) UNIQUE NOT NULL,
            PRIMARY KEY (DepartmentID)
        )
        """
        cursor.execute(create_departments_table)

        # Create table for Faculty
        create_faculty_table = """
        CREATE TABLE IF NOT EXISTS Faculty (
            FacultyID INT AUTO_INCREMENT PRIMARY KEY,
            FacultyName VARCHAR(255) NOT NULL,
            FacultyEmail VARCHAR(255) NOT NULL,
            FacultyRank ENUM('full', 'associate', 'assistant', 'adjunct') NOT NULL,
            DepartmentID INT,
            FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
        )
        """
        cursor.execute(create_faculty_table)

        # First creating all the tables

        create_programs_table = """
        CREATE TABLE IF NOT EXISTS Programs(
            ProgramID INT  AUTO_INCREMENT PRIMARY KEY,
            ProgramName VARCHAR(255),
            ProgramCoordinatorID INT,
            ProgramCoordinatorName VARCHAR(255),
            ProgramCoordinatorUniversityID VARCHAR(20),
            ProgramCoordinatorEmail VARCHAR(255),
            CONSTRAINT fk_Coordinator FOREIGN KEY (ProgramCoordinatorID) REFERENCES Faculty(FacultyID)

               )
               """
        cursor.execute(create_programs_table)

        # Create course table
        create_course_table = """
        CREATE TABLE IF NOT EXISTS Courses(
            CourseID VARCHAR(8) PRIMARY KEY,
            CourseTitle VARCHAR(255),
            CourseDescription TEXT,
            DepartmentID INT,
            FOREIGN KEY(DepartmentID) REFERENCES Departments(DepartmentID)
        )
        """
        cursor.execute(create_course_table)

        # Create a semester table.
        create_sections_table = """
        CREATE TABLE IF NOT EXISTS Sections (
            SectionID INT AUTO_INCREMENT,
            CourseID VARCHAR(8),
            SectionNumber INT,
            Semester ENUM('Fall', 'Spring', 'Summer'),
            Year INT,
            FacultyID INT,
            EnrolledStudents INT,
            PRIMARY KEY (SectionID),
            FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
            FOREIGN KEY (FacultyID) REFERENCES Faculty(FacultyID)
            )
            """
        cursor.execute(create_sections_table)

        # LearningObjectiveTable.
        create_lo_table = """
        CREATE TABLE IF NOT EXISTS LearningObjectives(
        LOCode INT AUTO_INCREMENT PRIMARY KEY,
        ProgramID INT,
        LODescription TEXT,
        CONSTRAINT fk_LoProgram FOREIGN KEY (ProgramID) REFERENCES Programs(ProgramID)
        )
        """
        cursor.execute(create_lo_table)

        # Create Subjective table

        create_sub_table = """
        CREATE TABLE IF NOT EXISTS SubObjectives(
        SubObjectiveCode INT AUTO_INCREMENT PRIMARY KEY,
        LOCode INT,
        SubObjectiveDescription TEXT,
        CONSTRAINT fk_SubObjectiveLO FOREIGN KEY (LOCode) REFERENCES LearningObjectives(LOCode)
    )
    """
        cursor.execute(create_sub_table)

    # Create the Program Courses Table
        create_programs_course_table = """
        CREATE TABLE IF NOT EXISTS ProgramCourses(
        ProgramID INT,
        CourseID VARCHAR(8),
        CONSTRAINT fk_ProgramCourseProgram FOREIGN KEY (ProgramID) REFERENCES Programs(ProgramID),
        CONSTRAINT fk_ProgramCourseCourse FOREIGN KEY (CourseID) REFERENCES Courses (CourseID)
    )
    """
        cursor.execute(create_programs_course_table)

    # Creating ObjectiveCourseSectionTable
        create_objectiveCS_table = """
        CREATE TABLE IF NOT EXISTS ObjectiveCourseSections(
        ObjectiveID INT,
        SectionID INT,
        EvaluationMethod VARCHAR(255),
        StudentsMetObjectives INT,
        CONSTRAINT fk_OCSObjective FOREIGN KEY (ObjectiveID) REFERENCES SubObjectives(SubObjectiveCode),
        CONSTRAINT fk_OCSSection FOREIGN KEY (SectionID) REFERENCES Sections(SectionID)
    )
    """
        cursor.execute(create_objectiveCS_table)

    connection.commit()

finally:
    connection.close()

print("Database and tables created successfully.")


if __name__ == '__main__':
    app.run(debug=True)

