"""Modern desktop interface for the Kenyan Students Grade Calculator."""

from __future__ import annotations

import csv
import tkinter as tk
from dataclasses import dataclass
from tkinter import filedialog, messagebox, ttk


SUBJECTS = ("Mathematics", "Science", "English")
COLORS = {"navy": "#102A43", "green": "#16866A", "cream": "#F7FAFC", "white": "#FFFFFF", "text": "#243B53", "muted": "#627D98"}


@dataclass
class StudentResult:
    name: str
    student_class: str
    scores: dict[str, float]
    total: float
    average: float
    grade: str


def get_grade(average: float) -> str:
    if average >= 80:
        return "A"
    if average >= 60:
        return "B"
    if average >= 40:
        return "C"
    return "D"


class GradeCalculatorApp(tk.Tk):
    """A polished, scalable interface for entering and reviewing results."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Kenyan Students Grade Calculator")
        self.geometry("1050x680")
        self.minsize(900, 600)
        self.configure(bg=COLORS["cream"])
        self.results: list[StudentResult] = []
        self._make_styles()
        self._make_variables()
        self._build_header()
        self._build_form()
        self._build_results()
        self._build_footer()

    def _make_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("App.TFrame", background=COLORS["cream"])
        style.configure("Card.TFrame", background=COLORS["white"])
        style.configure("Title.TLabel", background=COLORS["navy"], foreground=COLORS["white"], font=("Segoe UI", 22, "bold"))
        style.configure("Subtitle.TLabel", background=COLORS["navy"], foreground="#D9E2EC", font=("Segoe UI", 10))
        style.configure("Section.TLabel", background=COLORS["white"], foreground=COLORS["text"], font=("Segoe UI", 12, "bold"))
        style.configure("Field.TLabel", background=COLORS["white"], foreground=COLORS["muted"], font=("Segoe UI", 9, "bold"))
        style.configure("StatValue.TLabel", background=COLORS["white"], foreground=COLORS["navy"], font=("Segoe UI", 18, "bold"))
        style.configure("StatName.TLabel", background=COLORS["white"], foreground=COLORS["muted"], font=("Segoe UI", 9))
        style.configure("Primary.TButton", background=COLORS["green"], foreground=COLORS["white"], font=("Segoe UI", 10, "bold"), padding=(14, 8))
        style.configure("Secondary.TButton", background=COLORS["white"], foreground=COLORS["navy"], font=("Segoe UI", 10), padding=(12, 8))
        style.configure("Treeview", background=COLORS["white"], fieldbackground=COLORS["white"], foreground=COLORS["text"], rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background=COLORS["navy"], foreground=COLORS["white"], font=("Segoe UI", 9, "bold"), padding=8)

    def _make_variables(self) -> None:
        self.name_var = tk.StringVar()
        self.class_var = tk.StringVar()
        self.score_vars = {subject: tk.StringVar() for subject in SUBJECTS}
        self.student_count_var = tk.StringVar(value="0")
        self.class_average_var = tk.StringVar(value="0.00")
        self.top_grade_var = tk.StringVar(value="-")
        self.status_var = tk.StringVar(value="Ready for a new student")

    def _build_header(self) -> None:
        banner = tk.Frame(self, bg=COLORS["navy"], height=112)
        banner.pack(fill="x")
        banner.pack_propagate(False)
        ttk.Label(banner, text="KENYAN STUDENTS", style="Title.TLabel").pack(anchor="w", padx=28, pady=(20, 0))
        ttk.Label(banner, text="Grade Calculator  •  Built for classes of any size", style="Subtitle.TLabel").pack(anchor="w", padx=30, pady=(2, 0))

    def _build_form(self) -> None:
        card = ttk.Frame(self, style="Card.TFrame", padding=20)
        card.pack(fill="x", padx=24, pady=(20, 12))
        ttk.Label(card, text="Add student result", style="Section.TLabel").grid(row=0, column=0, columnspan=5, sticky="w", pady=(0, 14))
        self._field(card, "Student name", self.name_var, 1, 0)
        self._field(card, "Class / stream", self.class_var, 1, 1)
        for index, subject in enumerate(SUBJECTS, start=2):
            self._field(card, f"{subject} mark", self.score_vars[subject], 1, index)
        buttons = ttk.Frame(card, style="Card.TFrame")
        buttons.grid(row=2, column=0, columnspan=5, sticky="e", pady=(8, 0))
        ttk.Button(buttons, text="Add student", style="Primary.TButton", command=self.add_student).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Clear form", style="Secondary.TButton", command=self.clear_form).pack(side="left")
        for column in range(5):
            card.columnconfigure(column, weight=1)

    def _field(self, parent: ttk.Frame, label: str, variable: tk.StringVar, row: int, column: int) -> None:
        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.grid(row=row, column=column, sticky="ew", padx=(0, 12), pady=(0, 8))
        ttk.Label(frame, text=label.upper(), style="Field.TLabel").pack(anchor="w")
        ttk.Entry(frame, textvariable=variable, font=("Segoe UI", 11)).pack(fill="x", ipady=5, pady=(4, 0))

    def _build_results(self) -> None:
        container = ttk.Frame(self, style="App.TFrame")
        container.pack(fill="both", expand=True, padx=24, pady=4)
        stats = ttk.Frame(container, style="Card.TFrame", padding=14)
        stats.pack(fill="x", pady=(0, 12))
        self._stat(stats, "Students added", self.student_count_var, 0)
        self._stat(stats, "Class average", self.class_average_var, 1)
        self._stat(stats, "Top grade", self.top_grade_var, 2)
        for column in range(3):
            stats.columnconfigure(column, weight=1)
        table_card = ttk.Frame(container, style="Card.TFrame", padding=14)
        table_card.pack(fill="both", expand=True)
        ttk.Label(table_card, text="Class results", style="Section.TLabel").pack(anchor="w", pady=(0, 8))
        columns = ("number", "name", "class", "math", "science", "english", "total", "average", "grade")
        self.table = ttk.Treeview(table_card, columns=columns, show="headings", selectmode="browse")
        headings = {"number": "#", "name": "Student", "class": "Class", "math": "Math", "science": "Science", "english": "English", "total": "Total", "average": "Average", "grade": "Grade"}
        for column in columns:
            self.table.heading(column, text=headings[column])
            self.table.column(column, width=80 if column != "name" else 190, anchor="center" if column != "name" else "w")
        scrollbar = ttk.Scrollbar(table_card, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _stat(self, parent: ttk.Frame, label: str, variable: tk.StringVar, column: int) -> None:
        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.grid(row=0, column=column, sticky="w", padx=18)
        ttk.Label(frame, textvariable=variable, style="StatValue.TLabel").pack(anchor="w")
        ttk.Label(frame, text=label, style="StatName.TLabel").pack(anchor="w")

    def _build_footer(self) -> None:
        footer = ttk.Frame(self, style="App.TFrame", padding=(24, 8, 24, 16))
        footer.pack(fill="x")
        ttk.Label(footer, textvariable=self.status_var, foreground=COLORS["muted"], background=COLORS["cream"]).pack(side="left")
        ttk.Button(footer, text="Export CSV", style="Secondary.TButton", command=self.export_csv).pack(side="right")

    def add_student(self) -> None:
        name = self.name_var.get().strip()
        student_class = self.class_var.get().strip() or "-"
        if not name:
            self._show_error("Please enter the student's name.")
            return
        try:
            scores = {subject: float(self.score_vars[subject].get()) for subject in SUBJECTS}
        except ValueError:
            self._show_error("Enter a valid number for every subject mark.")
            return
        if any(score < 0 or score > 100 for score in scores.values()):
            self._show_error("Every mark must be between 0 and 100.")
            return
        total = sum(scores.values())
        average = total / len(SUBJECTS)
        result = StudentResult(name, student_class, scores, total, average, get_grade(average))
        self.results.append(result)
        self.table.insert("", "end", values=(len(self.results), name, student_class, f"{scores['Mathematics']:.1f}", f"{scores['Science']:.1f}", f"{scores['English']:.1f}", f"{total:.1f}", f"{average:.2f}", result.grade))
        self._update_stats()
        self.clear_form(show_status=False)
        self.status_var.set(f"Saved {name}. {len(self.results)} student(s) recorded.")

    def clear_form(self, show_status: bool = True) -> None:
        self.name_var.set("")
        self.class_var.set("")
        for variable in self.score_vars.values():
            variable.set("")
        if show_status:
            self.status_var.set("Form cleared")

    def _update_stats(self) -> None:
        self.student_count_var.set(str(len(self.results)))
        average = sum(result.average for result in self.results) / len(self.results)
        self.class_average_var.set(f"{average:.2f}")
        self.top_grade_var.set(max((result.grade for result in self.results), default="-", key="ABCD".index))

    def export_csv(self) -> None:
        if not self.results:
            self._show_error("Add at least one student before exporting.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")), initialfile="student_grade_report.csv")
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(("Name", "Class", *SUBJECTS, "Total", "Average", "Grade"))
            for result in self.results:
                writer.writerow((result.name, result.student_class, *(result.scores[subject] for subject in SUBJECTS), result.total, result.average, result.grade))
        self.status_var.set(f"Report exported to {path}")
        messagebox.showinfo("Export complete", "The student report was exported successfully.")

    def _show_error(self, message: str) -> None:
        self.status_var.set(message)
        messagebox.showerror("Check your input", message)


if __name__ == "__main__":
    GradeCalculatorApp().mainloop()
