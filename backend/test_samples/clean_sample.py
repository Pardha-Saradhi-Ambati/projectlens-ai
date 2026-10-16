def calculate_student_grade(scores: list[float], bonus_points: float = 0.0) -> dict:
    """
    Computes weighted average and letter grade for a student.
    Follows secure coding standards with defensive validation.
    """
    if not isinstance(scores, list) or len(scores) == 0:
        raise ValueError("Scores list must not be empty")

    for score in scores:
        if not isinstance(score, (int, float)) or score < 0 or score > 100:
            raise ValueError(f"Invalid score value: {score}. Must be between 0 and 100.")

    average = sum(scores) / len(scores) + max(0.0, bonus_points)
    
    if average >= 90.0:
        grade = "A"
    elif average >= 80.0:
        grade = "B"
    elif average >= 70.0:
        grade = "C"
    elif average >= 60.0:
        grade = "D"
    else:
        grade = "F"

    return {
        "average": round(average, 2),
        "letter_grade": grade,
        "total_assessments": len(scores)
    }
