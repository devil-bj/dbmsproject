from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Database connection parameters
host = 'localhost'
user = 'root'
password = 'American.1@#@'
db_name = 'university_db'


def get_db_connection():
    return pymysql.connect(host=host, user=user, password=password, db=db_name)


# This is my home screen where how query can be done is listed.
@app.route('/')
def home():
    return render_template('home.html')


# This line of code will store department info in to the database
@app.route('/departments')
def departments():
    return render_template('departments.html')


@app.route('/add_department', methods=['POST'])
def add_department():
    dept_name = request.form['deptName']
    dept_code = request.form['deptCode']

    # Insert data into the database
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO Departments (DepartmentName, DepartmentCode) VALUES (%s, %s)"
            cursor.execute(sql, (dept_name, dept_code))
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for('departments'))


# This line of code will store Faculty info into the database

@app.route('/faculty')
def faculty():
    return render_template('faculty.html')


@app.route('/add_faculty', methods=['POST'])
def add_faculty():
    # Extract data from form
    faculty_name = request.form['facultyName']
    faculty_email = request.form['facultyEmail']
    faculty_rank = request.form['facultyRank']
    department_id = request.form['departmentId']

    # Insert data into the database
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO Faculty (FacultyName, FacultyEmail, FacultyRank, DepartmentID)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (faculty_name, faculty_email, faculty_rank, department_id))
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for('faculty'))


# This line of code will store programs info
@app.route('/programs')
def programs():
    return render_template('programs.html')


@app.route('/add_program', methods=['POST'])
def add_program():
    program_name = request.form['programName']
    program_coordinator_id = request.form['programCoordinatorId']
    program_coordinator_name = request.form['programCoordinatorName']
    program_coordinator_university_id = request.form['programCoordinatorUniversityID']
    program_coordinator_email = request.form['programCoordinatorEmail']

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO Programs (ProgramName, ProgramCoordinatorID, ProgramCoordinatorName, ProgramCoordinatorUniversityID, ProgramCoordinatorEmail)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                program_name, program_coordinator_id, program_coordinator_name, program_coordinator_university_id,
                program_coordinator_email))
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for('programs'))


# Courses Can be added here...
@app.route('/courses')
def courses():
    return render_template('courses.html')


@app.route('/add_course', methods=['POST'])
def add_course():
    course_id = request.form['courseId']
    course_title = request.form['courseTitle']
    course_description = request.form['courseDescription']
    department_id = request.form['departmentId']

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO Courses (CourseID, CourseTitle, CourseDescription, DepartmentID)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (course_id, course_title, course_description, department_id))
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for('courses'))


# This line of code allows data to be added to the database using html form.
@app.route('/sections')
def sections():
    return render_template('sections.html')


@app.route('/add_section', methods=['POST'])
def add_section():
    course_id = request.form['courseId']
    section_number = request.form['sectionNumber']
    semester = request.form['semester']
    year = request.form['year']
    faculty_id = request.form['facultyId']
    enrolled_students = request.form['enrolledStudents']

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO Sections (CourseID, SectionNumber, Semester, Year, FacultyID, EnrolledStudents)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (course_id, section_number, semester, year, faculty_id, enrolled_students))
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for('sections'))


# Here Learning objectives are collected.
@app.route('/learning')
def learning_objectives():
    return render_template('learning_objectives.html')


@app.route('/add_learning_objective', methods=['POST'])
def add_learning_objective():
    program_id = request.form['programId']
    lo_description = request.form['loDescription']

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO LearningObjectives (ProgramID, LODescription)
            VALUES (%s, %s)
            """
            cursor.execute(sql, (program_id, lo_description))
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for('learning_objectives'))


# This line of code allows subjective data to be added to the database using html form.

@app.route('/sub_objectives')
def sub_objectives():
    return render_template('sub_objectives.html')


@app.route('/add_sub_objective', methods=['POST'])
def add_sub_objective():
    lo_code = request.form['loCode']
    sub_objective_description = request.form['subObjectiveDescription']

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO SubObjectives (LOCode, SubObjectiveDescription)
            VALUES (%s, %s)
            """
            cursor.execute(sql, (lo_code, sub_objective_description))
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for('sub_objectives'))


# This line of code allows assigning courses to the program and adds to the database using html form.
@app.route('/program_courses')
def program_courses():
    return render_template('program_courses.html')


@app.route('/add_program_course', methods=['POST'])
def add_program_course():
    program_id = request.form['programId']
    course_id = request.form['courseId']

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO ProgramCourses (ProgramID, CourseID)
            VALUES (%s, %s)
            """
            cursor.execute(sql, (program_id, course_id))
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for('program_courses'))


# This line of code allows assigning learning objectives to (course, program) pairs and the database stored using
# html form.
@app.route('/objective_course_sections')
def objective_course_sections():
    return render_template('objective_course_sections.html')


@app.route('/add_objective_course_section', methods=['POST'])
def add_objective_course_section():
    objective_id = request.form['objectiveId']
    section_id = request.form['sectionId']
    evaluation_method = request.form['evaluationMethod']
    students_met_objectives = request.form['studentsMetObjectives']

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO ObjectiveCourseSections (ObjectiveID, SectionID, EvaluationMethod, StudentsMetObjectives)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (objective_id, section_id, evaluation_method, students_met_objectives))
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for('objective_course_sections'))


# Fetching of data can be done here
@app.route('/query_departments', methods=['GET', 'POST'])
def query_departments():
    conn = get_db_connection()
    departments = None
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT DepartmentID, DepartmentName FROM Departments")
            departments = cursor.fetchall()
    finally:
        conn.close()

    if request.method == 'POST':
        department_id = request.form.get('departmentId')
        if department_id:
            return redirect(url_for('list_programs_faculty', department_id=department_id))

    # Ensure that we are actually getting data back
    print(departments)

    return render_template('query_departments.html', departments=departments)


# Fetching the Given department using html form:
#  List all its program
#  List all its faculty (including what program each faculty is in charge of, if there is one)

@app.route('/list_programs_faculty/<int:department_id>')
def list_programs_faculty(department_id):
    programs = []
    faculty = []
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # This query should join Programs with Faculty and then with Departments
            cursor.execute("""
                SELECT Programs.ProgramID, Programs.ProgramName
                FROM Programs
                JOIN Faculty ON Programs.ProgramCoordinatorID = Faculty.FacultyID
                WHERE Faculty.DepartmentID = %s
            """, (department_id,))
            programs = cursor.fetchall()

            # This query should select all faculty within the specified department
            cursor.execute("""
                SELECT Faculty.FacultyName, Programs.ProgramName
                FROM Faculty
                LEFT JOIN Programs ON Faculty.FacultyID = Programs.ProgramCoordinatorID
                WHERE Faculty.DepartmentID = %s
            """, (department_id,))
            faculty = cursor.fetchall()
    finally:
        conn.close()
    print(programs)
    print(faculty)

    return render_template('list_programs_faculty.html', programs=programs, faculty=faculty)


# It shows following details:Given a program:
# List all the courses, together with the objectives/sub-objectives association with year
# List all the objectives

@app.route('/program_details/<int:program_id>')
def program_details(program_id):
    conn = get_db_connection()
    courses = []
    objectives = []
    course_objectives = []

    try:
        with conn.cursor() as cursor:
            # Query to list all courses for the given program
            cursor.execute("""
                SELECT Courses.CourseID, Courses.CourseTitle FROM Courses
                JOIN ProgramCourses ON Courses.CourseID = ProgramCourses.CourseID
                WHERE ProgramCourses.ProgramID = %s
            """, (program_id,))
            courses = cursor.fetchall()

            # Query to list all objectives for the given program
            cursor.execute("""
                SELECT LOCode, LODescription FROM LearningObjectives
                WHERE ProgramID = %s
            """, (program_id,))
            objectives = cursor.fetchall()

            # Query to list all course objectives/sub-objectives with year
            cursor.execute("""
                SELECT Courses.CourseID, Courses.CourseTitle, 
                       LearningObjectives.LODescription, SubObjectives.SubObjectiveDescription,
                       Sections.Year
                FROM Courses
                JOIN ProgramCourses ON Courses.CourseID = ProgramCourses.CourseID
                JOIN Sections ON Courses.CourseID = Sections.CourseID
                JOIN ObjectiveCourseSections ON Sections.SectionID = ObjectiveCourseSections.SectionID
                JOIN SubObjectives ON ObjectiveCourseSections.ObjectiveID = SubObjectives.SubObjectiveCode
                JOIN LearningObjectives ON SubObjectives.LOCode = LearningObjectives.LOCode
                WHERE ProgramCourses.ProgramID = %s
                GROUP BY Sections.SectionID, SubObjectives.SubObjectiveCode
            """, (program_id,))
            course_objectives = cursor.fetchall()

    finally:
        conn.close()
        print(courses)
        print(objectives)
        print(course_objectives)

    return render_template('program_details.html', courses=courses, objectives=objectives,
                           course_objectives=course_objectives)


# This line of code do the following:
# Given a semester and a program:
# List all the evaluation results for each section.
# (If data for some sections has not been entered, just indicate that the information is not found)

@app.route('/final_results/<int:program_id>/<semester>')
def evaluation_results(program_id, semester):
    conn = get_db_connection()
    section_results = []

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT Sections.SectionID, Courses.CourseTitle, Sections.SectionNumber, 
                       Sections.Semester, Sections.Year, 
                       ObjectiveCourseSections.EvaluationMethod, 
                       ObjectiveCourseSections.StudentsMetObjectives
                FROM Sections
                JOIN Courses ON Sections.CourseID = Courses.CourseID
                JOIN ProgramCourses ON Courses.CourseID = ProgramCourses.CourseID
                LEFT JOIN ObjectiveCourseSections ON Sections.SectionID = ObjectiveCourseSections.SectionID
                WHERE ProgramCourses.ProgramID = %s AND Sections.Semester = %s
            """, (program_id, semester))
            section_results = cursor.fetchall()

    finally:
        conn.close()

    # If there is no data for some sections, we add a placeholder
    section_results_with_info = [
        result if result else ("Information not found",) * 6
        for result in section_results
    ]

    return render_template('evaluation_results.html', section_results=section_results_with_info, semester=semester)


# This line of code perform following things: Given an academic year (e.g. 23-24, which constitute summer 23,
# fall 23 and spring 24) List all the evaluation results for each objective/sub-objective For each
# objective/sub-objective, list the course/section that are involved in evaluating them, and list the result for each
# course/section. For each objective/sub-objective, aggregate the result to show the number (and the percentage) of
# students

@app.route('/evaluation_results/<academic_year>', endpoint='unique_evaluation_results')
def evaluation_results(academic_year):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Assuming academic year '23-24' translates to '2023' and '2024'
            year_start, year_end = academic_year.split('-')
            year_start = '20' + year_start
            year_end = '20' + year_end

            cursor.execute("""
                SELECT ObjectiveCourseSections.ObjectiveID, SubObjectives.SubObjectiveDescription, 
                       Courses.CourseTitle, Sections.SectionNumber, Sections.Semester, 
                       ObjectiveCourseSections.StudentsMetObjectives
                FROM ObjectiveCourseSections
                JOIN SubObjectives ON ObjectiveCourseSections.ObjectiveID = SubObjectives.SubObjectiveCode
                JOIN Sections ON ObjectiveCourseSections.SectionID = Sections.SectionID
                JOIN Courses ON Sections.CourseID = Courses.CourseID
                WHERE Sections.Year = %s OR Sections.Year = %s
            """, (year_start, year_end))
            raw_data = cursor.fetchall()

    finally:
        conn.close()

    organized_data = organize_data(raw_data)
    return render_template('final_results.html', organized_data=organized_data, academic_year=academic_year)


def organize_data(raw_data):
    organized = {}
    for row in raw_data:
        objective_id, sub_obj_desc, course_title, section_number, semester, students_met = row
        key = (objective_id, sub_obj_desc)

        if key not in organized:
            organized[key] = {'sections': [], 'total_students': 0, 'students_met': 0}

        organized[key]['sections'].append({
            'course_title': course_title,
            'section_number': section_number,
            'semester': semester,
            'students_met': students_met
        })
        organized[key]['total_students'] += students_met
        organized[key]['students_met'] += students_met  # Adjust this logic based on your data

    # Calculate percentages
    for obj in organized.values():
        obj['percentage'] = (obj['students_met'] / obj['total_students'] * 100) if obj['total_students'] > 0 else 0

    return organized
