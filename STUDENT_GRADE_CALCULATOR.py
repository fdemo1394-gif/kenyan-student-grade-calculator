"""Kenyan students' grade calculator."""

from dataclasses import dataclass


SUBJECTS = ("Mathematics", "Science", "English")


@dataclass
class StudentResult:
    """The calculated result for one student."""

    name: str
    student_class: str
    scores: dict[str, float]
    total: float
    average: float
    grade: str


def get_grade(average: float) -> str:
    """Return the grade for a mean score out of 100."""
    if average >= 80:
        return "A"
    if average >= 60:
        return "B"
    if average >= 40:
        return "C"
    return "D"


def get_score(subject: str) -> float:
    """Read and validate one subject score."""
    while True:
        try:
            score = float(input(f"Enter {subject} score (0-100): "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if 0 <= score <= 100:
            return score
        print("Score must be between 0 and 100.")


def print_report(results: list[StudentResult]) -> None:
    """Print every result and a summary for the class."""
    if not results:
        print("\nNo student records were entered.")
        return

    print("\n" + "=" * 72)
    print("KENYAN STUDENTS' GRADE REPORT")
    print("=" * 72)
    print(f"{'No.':<5}{'Name':<25}{'Class':<12}{'Total':>10}{'Average':>10}{'Grade':>8}")
    print("-" * 72)

    for number, result in enumerate(results, start=1):
        print(
            f"{number:<5}{result.name[:24]:<25}{result.student_class[:11]:<12}"
            f"{result.total:>10.2f}{result.average:>10.2f}{result.grade:>8}"
        )

    class_average = sum(result.average for result in results) / len(results)
    grade_counts = {grade: sum(result.grade == grade for result in results) for grade in "ABCD"}
    print("-" * 72)
    print(f"Students: {len(results)}")
    print(f"Class average: {class_average:.2f}")
    print("Grade distribution: " + ", ".join(f"{g}: {n}" for g, n in grade_counts.items()))


def main() -> None:
    """Collect students until the user chooses to finish."""
    results: list[StudentResult] = []
    print("Kenyan Students' Grade Calculator")
    print("Enter 'done' as the student name when you have finished.\n")

    while True:
        name = input("Enter student name (or 'done' to finish): ").strip()
        if name.lower() == "done":
            break
        if not name:
            print("Student name cannot be empty.")
            continue

        student_class = input("Enter student class: ").strip()
        scores = {subject: get_score(subject) for subject in SUBJECTS}
        total = sum(scores.values())
        average = total / len(SUBJECTS)
        results.append(
            StudentResult(name, student_class, scores, total, average, get_grade(average))
        )
        print(f"Saved {len(results)} student(s).")

    print_report(results)


if __name__ == "__main__":
    main()
