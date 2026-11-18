# Kenyan Students Grade Calculator

A Python command-line application for calculating student totals, averages, grades, and class statistics.

## Features

- Handles any number of students, including classes with more than 80 students
- Includes a responsive browser version built with HTML, CSS, and JavaScript
- Includes a modern desktop interface built with Tkinter
- Accepts Mathematics, Science, and English scores
- Validates scores between 0 and 100
- Assigns grades based on the average score
- Displays a complete class report
- Calculates the class average and grade distribution
- Exports class results to CSV

## Grade scale

| Average score | Grade |
| --- | --- |
| 80–100 | A |
| 60–79 | B |
| 40–59 | C |
| 0–39 | D |

## Requirements

- Python 3.9 or later

## Run the desktop application

```bash
python app.py
```

Use the desktop form to add students, review live statistics, and export a CSV report.

## Open the web version

Open `index.html` in a browser. The web version includes responsive styling, live class statistics, input validation, and CSV export. Keep `styles.css` and `script.js` in the same folder as `index.html`.

## Run the command-line version

```bash
python STUDENT_GRADE_CALCULATOR.py
```

Enter `done` as the student name when all students have been added.

## Project purpose

This project demonstrates Python input validation, data classes, loops, collections, functions, and basic class-level data analysis.
