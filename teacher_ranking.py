
import streamlit as st
import pandas as pd

def show_teacher_ranking():
    st.title("Teacher Ranking & Analysis")

    # Load the dataset
    df = pd.read_csv('eval3.csv', encoding='cp1252')

    # Custom CSS for beautiful table and page design
    st.markdown("""
        <style>
            .main-title {
                font-size: 36px;
                font-weight: bold;
                text-align: center;
                color: #0D47A1;
                margin-bottom: 10px;
            }
            .subheader {
                font-size: 24px;
                font-weight: bold;
                color: #1565C0;
                margin: 10px 0;
                border-bottom: 2px solid #0D47A1;
                padding-bottom: 5px;
            }
            .stSelectbox label {
                font-weight: bold;
                color: #0D47A1;
                font-size: 16px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            }
            th {
                background-color: #0D47A1;
                color: white;
                padding: 12px;
                font-size: 14px;
                text-transform: uppercase;
                text-align: left;
            }
            tr:nth-child(even) {
                background-color: #f1f1f1;
            }
            tr:nth-child(odd) {
                background-color: #ffffff;
            }
            td {
                padding: 10px;
                font-size: 14px;
                color: #444;
            }
            tr:hover {
                background-color: #E3F2FD;
            }
        </style>
    """, unsafe_allow_html=True)

    # Page Title
    st.markdown("<p class='main-title'>Teachers Evaluation - Analysis Dashboard</p>", unsafe_allow_html=True)

    # Dropdown for column selection (the 18 questions start from column 3 onwards)
    columns = list(df.columns[3:])
    selected_column = st.selectbox("Select Evaluation Question", columns)

    # Subheader for selected question ranking
    st.markdown(f"<p class='subheader'>🏅 Teachers Ranking for: {selected_column}</p>", unsafe_allow_html=True)

    # Calculate average score for selected question per teacher
    teacher_scores = df.groupby('Teacher')[selected_column].mean().reset_index()
    teacher_scores = teacher_scores.sort_values(selected_column, ascending=False)
    st.markdown(teacher_scores.to_html(index=False, escape=False), unsafe_allow_html=True)

    # --- Section Divider ---
    st.markdown("<hr style='border: 1px solid #0D47A1;'>", unsafe_allow_html=True)

    # 🌟 Best Teachers from Each Grade (Weighted Average)
    st.markdown("<p class='subheader'>🌟 Best Teachers from Each Grade (Weighted Average)</p>", unsafe_allow_html=True)

    # Compute weighted average
    question_columns = df.columns[3:]
    rating_columns = [col for col in question_columns if df[col].dropna().between(1, 5).all()]

    if 'Weight' in df.columns:
        weight_col = df['Weight']
    else:
        weight_col = pd.Series(1, index=df.index)

    weighted_scores = df[rating_columns].multiply(weight_col, axis=0)
    df['Weighted_Average'] = weighted_scores.sum(axis=1) / weight_col.sum()

    grade_teacher_avg = df.groupby(['Grade', 'Teacher'])['Weighted_Average'].mean().reset_index()
    best_teachers_per_grade = grade_teacher_avg.loc[grade_teacher_avg.groupby('Grade')['Weighted_Average'].idxmax()]

    st.markdown(best_teachers_per_grade.to_html(index=False, escape=False), unsafe_allow_html=True)

    # --- Section Divider ---
    st.markdown("<hr style='border: 1px solid #0D47A1;'>", unsafe_allow_html=True)

    # 🏅 Top Teachers Overall (Weighted)
    st.markdown("<p class='subheader'>🏅 Top Teachers Overall (All Grades, Weighted)</p>", unsafe_allow_html=True)

    overall_teacher_avg = df.groupby('Teacher')['Weighted_Average'].mean().reset_index()
    overall_teacher_avg = overall_teacher_avg.sort_values('Weighted_Average', ascending=False)
    st.markdown(overall_teacher_avg.to_html(index=False, escape=False), unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center; color:gray;'>Designed by Ammon - Data Analyst 2025</p>", unsafe_allow_html=True)
