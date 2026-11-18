const subjects = ['Mathematics', 'Science', 'English'];
const students = [];
const form = document.querySelector('#student-form');
const resultsBody = document.querySelector('#results-body');
const emptyState = document.querySelector('#empty-state');
const message = document.querySelector('#form-message');

function gradeFor(average) {
  if (average >= 80) return 'A';
  if (average >= 60) return 'B';
  if (average >= 40) return 'C';
  return 'D';
}

function readScore(id) {
  const value = Number(document.querySelector(`#${id}`).value);
  return Number.isFinite(value) && value >= 0 && value <= 100 ? value : null;
}

function render() {
  resultsBody.innerHTML = students.map((student, index) => `
    <tr><td>${index + 1}</td><td><strong>${student.name}</strong></td><td>${student.studentClass}</td>
    <td>${student.scores.Mathematics.toFixed(1)}</td><td>${student.scores.Science.toFixed(1)}</td><td>${student.scores.English.toFixed(1)}</td>
    <td><strong>${student.average.toFixed(2)}</strong></td><td><span class="grade">${student.grade}</span></td></tr>`).join('');
  emptyState.hidden = students.length > 0;
  document.querySelector('#student-count').textContent = students.length;
  const average = students.length ? students.reduce((sum, student) => sum + student.average, 0) / students.length : 0;
  document.querySelector('#class-average').textContent = average.toFixed(2);
  document.querySelector('#top-grade').textContent = students.length ? students.map((student) => student.grade).sort((a, b) => 'ABCD'.indexOf(a) - 'ABCD'.indexOf(b))[0] : '—';
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  message.textContent = '';
  const name = document.querySelector('#student-name').value.trim();
  const studentClass = document.querySelector('#student-class').value.trim() || '—';
  const scores = Object.fromEntries(subjects.map((subject) => [subject, readScore(subject.toLowerCase())]));
  if (!name) { message.textContent = 'Please enter the student name.'; return; }
  if (Object.values(scores).some((score) => score === null)) { message.textContent = 'Enter marks between 0 and 100 for all subjects.'; return; }
  const total = Object.values(scores).reduce((sum, score) => sum + score, 0);
  const average = total / subjects.length;
  students.push({ name, studentClass, scores, total, average, grade: gradeFor(average) });
  form.reset();
  render();
});

document.querySelector('#clear-form').addEventListener('click', () => { form.reset(); message.textContent = ''; });

document.querySelector('#export-csv').addEventListener('click', () => {
  if (!students.length) { message.textContent = 'Add at least one student before exporting.'; return; }
  const rows = [['Name', 'Class', ...subjects, 'Total', 'Average', 'Grade'], ...students.map((student) => [student.name, student.studentClass, ...subjects.map((subject) => student.scores[subject]), student.total.toFixed(2), student.average.toFixed(2), student.grade])];
  const csv = rows.map((row) => row.map((value) => `"${String(value).replaceAll('"', '""')}"`).join(',')).join('\n');
  const link = document.createElement('a');
  link.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }));
  link.download = 'student-grade-report.csv';
  link.click();
  URL.revokeObjectURL(link.href);
});

render();
