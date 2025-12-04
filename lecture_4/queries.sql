--create tables: students and grades
create table students(id integer primary key AUTOINCREMENT, full_name text, birth_year int);
create table grades(id integer primary key AUTOINCREMENT, student_id int REFERENCES students(id), 
subject text, grade int);

--insert the data into the tables
insert into students(full_name, birth_year) values ('Alice Johnson', 2005),
('Brian Smith', 2004),
('Carla Reyes', 2006),
('Daniel Kim', 2005),
('Eva Thompson', 2003),
('Felix Nguyen', 2007),
('Grace Patel', 2005),
('Henry Lopez', 2004),
('Isabella Martinez', 2006);

insert into grades (student_id, subject, grade) values 
(1, 'Math', 88),
(1, 'English', 92),
(1, 'Science', 85),
(2, 'Math', 75),
(2, 'History', 83),
(2, 'English', 79),
(3, 'Science', 95),
(3, 'Math', 91),
(3, 'Art', 89),
(4, 'Math', 84),
(4, 'Science', 88),
(4, 'Physical Education', 93),
(5, 'English', 90),
(5, 'History', 85),
(5, 'Math', 88),
(6, 'Science', 72),
(6, 'Math', 78),
(6, 'English', 81),
(7, 'Art', 94),
(7, 'Science', 87),
(7, 'Math', 90),
(8, 'History', 77),
(8, 'Math', 83),
(8, 'Science', 80),
(9, 'English', 96),
(9, 'Math', 89),
(9, 'Art', 92);

--find all grades for a spesific student(Alice Johnson)
select subject, grade from grades join students on grades.student_id = students.id 
where students.full_name = 'Alice Johnson';

--calculate the average grade per student
select student_id, avg(grade) as average_grade from grades group by student_id;

--list all students born after 2004
select * from students where birth_year > 2004;

--List all subjects and their average grades
select subject, avg(grade) as average_grade from grades group by subject;

--find the top 3 students with the highest average grades
select students.id, full_name from students join grades on students.id = grades.student_id 
group by students.id, full_name order by avg(grade) desc limit 3;

--Show all students who have scored below 80 in any subject
select distinct full_name from students join grades on students.id = grades.student_id where grades.grade < 80; 