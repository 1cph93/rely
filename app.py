import asyncio
import enum

import streamlit as st

from rely.services.score_repo_service import score_repo


class LetterGrade(enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"


def compute_letter_grade(numerical_grade: int) -> LetterGrade:
    if numerical_grade < 50:
        letter_grade = LetterGrade.F
    elif 50 <= numerical_grade < 60:
        letter_grade = LetterGrade.E
    elif 60 <= numerical_grade < 70:
        letter_grade = LetterGrade.D
    elif 70 <= numerical_grade < 80:
        letter_grade = LetterGrade.C
    elif 80 <= numerical_grade < 90:
        letter_grade = LetterGrade.B
    else:
        letter_grade = LetterGrade.A

    return letter_grade


def render() -> None:
    main_form = st.form("main_form")

    repo_owner = main_form.text_input("Repo Owner:", "1cph93")
    repo_name = main_form.text_input("Repo Name:", "bcolz")

    submit = main_form.form_submit_button("Analyze")

    # serialized_computed_metrics = [
    #     (computed_metric[0], computed_metric[-1].value)
    #     for computed_metric in repo_score.computed_metrics
    # ]

    if submit:
        repo_score = asyncio.run(score_repo(repo_owner, repo_name))
        numerical_grade = int(repo_score.overall_score * 100)
        letter_grade = compute_letter_grade(numerical_grade)
        main_form.subheader(f"Grade: {letter_grade.value} ({numerical_grade}%)")
        # st.table(data=serialized_computed_metrics)
    else:
        main_form.subheader("&nbsp;")


render()
