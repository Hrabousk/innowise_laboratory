def add_student(students: list[dict]) -> None:
    """
    Adds a new student to the system after validation.
    Prompts for student name, validates it's non-empty and unique, then creates
    a new student record with empty grades list.
    Args:
        students: List of student dictionaries to modify. Each student should have
                  'name' (str) and 'grades' (list[int]) keys.
    Returns:
        None
    Raises:
        No exceptions raised - invalid input handled via early return.
    Side effects:
        - Modifies students list by appending new student record
        - Prints prompts and status messages to stdout
    """
    print("Please enter the student's name")
    name: str = input().strip().capitalize()
    if name == "":
        print("Please enter anything as a name!")
        return
    for student in students:
        if student["name"] == name:
            print("A student with such a name already exists")
            return
    new_student: dict[str, str | list[int]] = {"name": name, "grades": []}
    print("Student added successfully!")
    students.append(new_student)


def add_a_grade(students: list[dict]) -> None:
    """
    Adds grades to an existing student's record interactively.
    Finds student by name and enters interactive grade entry loop. Validates
    each grade is integer between 0-100 before adding to student's record.
    Args:
        students: List of student dictionaries to search and modify.
    Returns:
        None
    Raises:
        No exceptions raised - invalid grades handled via continue in loop.
    Side effects:
        - Modifies student's grades list in-place
        - Prints prompts and status messages to stdout
    """
    if len(students) == 0:
        print("There are no students on the list")
        return
    print("Please enter the student's name")
    name: str = input().strip().capitalize()
    for student in students:
        if student["name"] == name:
            while True:
                print(
                    'Enter a valid grade (from 0 to 100, integer numbers) or "done" to finish'
                )
                choice: str = input().strip()
                if choice == "done":
                    print(
                        f"Finished successfully, {name}'s grades are: {student['grades']}"
                    )
                    return
                try:
                    grade_value: int = int(choice)
                except ValueError:
                    print("Enter an integer from 0 to 100")
                    continue
                if grade_value < 0 or grade_value > 100:
                    print("Enter an integer from 0 to 100")
                    continue
                student["grades"].append(grade_value)
    else:
        print("A student with such a name isn't found on the list")
        return


def show_report(students: list[dict]) -> None:
    """
    Generates and displays comprehensive student performance report.
    Calculates individual student averages, handles students with no grades,
    and computes class statistics including max, min, and overall average.
    Args:
        students: List of student dictionaries to analyze. Each student should
                  have 'name' (str) and 'grades' (list[int]) keys.
    Returns:
        None
    Raises:
        ZeroDivisionError: Handled internally when student has no grades.
    Side effects:
        - Prints formatted report with averages and statistics to stdout
    """
    na_counter: int = 0
    max_average: float = 0.0
    overall: float = 0.0
    min_average: float = 0.0
    first_average: bool = True
    if len(students) == 0:
        print("There are no students on the list")
        return
    for student in students:
        try:
            average: float = sum(student["grades"]) / len(student["grades"])
        except ZeroDivisionError:
            na_counter += 1
            print(f"{student['name']}'s average grade is N/A")
            continue
        print(f"{student['name']}'s average grade is {average}")
        overall += average
        if first_average:
            min_average = average
            first_average = False
        if average < min_average:
            min_average = average
        if average > max_average:
            max_average = average
    if na_counter == len(students):
        print("There are no students' grades on the list")
        return
    print(f"Max average: {max_average}")
    print(f"Min average: {min_average}")
    print(f"Overall average: {overall / (len(students) - na_counter)}")


def top_performer(students: list[dict]) -> None:
    """
    Identifies and displays students with the highest average grade.
    Calculates averages for all students with grades, finds maximum average,
    and displays all students achieving that maximum score.
    Args:
        students: List of student dictionaries to analyze. Each student should
                  have 'name' (str) and 'grades' (list[int]) keys.
    Returns:
        None
    Raises:
        ZeroDivisionError: Handled internally when student has no grades.
    Side effects:
        - Prints top performers list with averages and status messages to stdout
    """
    if len(students) == 0:
        print("There are no students on the list")
        return
    only_n_a: bool = True
    for student in students:
        if student.get("grades") and len(student["grades"]) > 0:
            only_n_a = False
    if only_n_a:
        print("There are no grades on the list")
        return
    top_performers: list[dict] = []
    key: float = max(
        list(
            map(
                lambda x: sum(x["grades"]) / len(x["grades"])
                if x.get("grades") and len(x["grades"]) > 0
                else -1,
                students,
            )
        )
    )
    for student in students:
        try:
            if sum(student["grades"]) / len(student["grades"]) == key:
                top_performers.append(student)
        except ZeroDivisionError:
            continue
    print("Top performers are: ")
    for student in top_performers:
        grades: list = student["grades"]
        average: float = sum(grades) / len(grades)
        print(f"{student['name']} having the average score of {average}")


"""
Student Grade Analyzer - Interactive grade management system.

Provides menu-driven interface for managing student records and grades.
Handles student creation, grade entry, reporting, and performance analysis.
"""
students: list[dict] = []
print(
    "Hello, user! This is a student grade analyzer!\nEnter the number on the left to perform the action on the right\n"
    "for the following:\n"
    "1. Add a new student\n"
    "2. Add a grade for a student\n"
    "3. Show report (all students)\n"
    "4. Find top performer\n"
    "5. Exit"
)
while True:
    try:
        choice: int = int(input())
    except ValueError:
        print("Please enter a valid number")
        continue
    match choice:
        case 1:
            add_student(students)
        case 2:
            add_a_grade(students)
        case 3:
            show_report(students)
        case 4:
            top_performer(students)
        case 5:
            print("Goodbye!")
            break
        case _:
            print("Please choose a valid option")
