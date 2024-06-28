--inserts a row into an existing column (must change the values in the second set of brackets)
INSERT INTO Courses (Id, CourseName, CourseThumbNail, CourseDescription, Difficulty, GameVersion) VALUES (3, 'Alarm System', 'ThumbNail', 'Uses tripwires or pressure plates to trigger a series of redstone lamps or note blocks, alerting players to intruders or other events.');

--deletes a row (must change the table and the line)
DELETE FROM Users WHERE Id > 1;

--Updates a row without having to delete it first)
UPDATE Courses SET Difficulty = 'Easy';

ALTER TABLE Courses
ADD Link TEXT;

--deletes a column from an existing table
ALTER TABLE Courses DROP UserId;

--creates a table
CREATE TABLE Courses (
    Id INTEGER PRIMARY KEY,
    CourseName TEXT,
    CourseThumbNail TEXT,
    CourseDescription TEXT
);

--deletes whole table
DROP TABLE Courses;

--add a column
ALTER TABLE Courses ADD GameVersion TEXT;


INSERT INTO Tasks (TaskId, CourseId, Task,) VALUES (1, '1', 'Place two redstone repeaters parallel to eachother, but make sure that they are both pointing different ways');
