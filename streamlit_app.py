import streamlit as st
from app import analyze_classroom_audio

st.set_page_config(page_title="Classroom Voice Analytics MVP", layout="wide")

st.title("Classroom Voice Analytics MVP")
st.write("Upload a classroom audio file to view transcript, metrics, and summary.")

uploaded_file = st.file_uploader("Upload audio file", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    with open("temp_audio.mp3", "wb") as f:
        f.write(uploaded_file.read())

    st.info("Analyzing audio... please wait.")

    output = analyze_classroom_audio("temp_audio.mp3")

    st.success(f"Detected Language: {output['language']}")

    st.subheader("Original Transcript")
    st.caption("Note: Original transcript may be noisy due to classroom audio.")
    st.write(output["raw_transcript"])

    st.subheader("Translated Transcript (English)")
    st.write(output["transcript"])

    st.subheader("Teacher vs Student Speech")
    c1, c2 = st.columns(2)
    c1.metric("Teacher Speech", f'{output["teacher_words"]} words', f'{output["teacher_speech_percent"]:.2f}%')
    c2.metric("Student Speech", f'{output["student_words"]} words', f'{output["student_speech_percent"]:.2f}%')

    st.subheader("Classroom Analysis")
    c3, c4, c5, c6 = st.columns(4)
    c3.metric("Teacher Talk Time", f'{output["teacher_time"]:.2f} sec')
    c4.metric("Student Talk Time", f'{output["student_time"]:.2f} sec')
    c5.metric("Questions Asked", output["questions"])
    c6.metric("Student Responses", output["student_responses"])

    st.subheader("Engagement Metrics")
    c7, c8, c9 = st.columns(3)
    c7.metric("Teacher Dominance Ratio", f'{output["teacher_dominance"]:.2f}')
    c8.metric("Student Participation Indicator", f'{output["student_participation"]:.2f}')
    c9.metric("Interaction Count", output["interaction_count"])

    st.subheader("Silence Analysis")
    c10, c11 = st.columns(2)
    c10.metric("Silence Duration", f'{output["silence_time"]:.2f} sec')
    c11.metric("Silence Ratio", f'{output["silence_ratio"]:.2f}')

    st.subheader("Short Classroom Summary")

    summary = []

    if output["teacher_dominance"] > 0.7:
        summary.append("Teacher dominated most of the classroom interaction.")
    else:
        summary.append("Teacher and students both contributed to the interaction.")

    if output["student_participation"] < 0.3:
        summary.append("Student participation was relatively low.")
    else:
        summary.append("Student participation was reasonably active.")

    if output["silence_ratio"] > 0.3:
        summary.append("The classroom had noticeable silence gaps.")
    else:
        summary.append("Silence gaps were limited.")

    for point in summary:
        st.write(f"- {point}")

    #  Download Button
    report_text = f"""
Classroom Voice Analytics MVP Report

Detected Language: {output['language']}

Original Transcript:
{output['raw_transcript']}

Translated Transcript (English):
{output['transcript']}

Teacher vs Student Speech:
Teacher Speech: {output['teacher_words']} words ({output['teacher_speech_percent']:.2f}%)
Student Speech: {output['student_words']} words ({output['student_speech_percent']:.2f}%)

Classroom Analysis:
Teacher Talk Time: {output['teacher_time']:.2f} sec
Student Talk Time: {output['student_time']:.2f} sec
Questions Asked: {output['questions']}
Student Responses: {output['student_responses']}

Engagement Metrics:
Teacher Dominance Ratio: {output['teacher_dominance']:.2f}
Student Participation Indicator: {output['student_participation']:.2f}
Interaction Count: {output['interaction_count']}

Silence Analysis:
Silence Duration: {output['silence_time']:.2f} sec
Silence Ratio: {output['silence_ratio']:.2f}
"""

    st.download_button(
        label="Download Report",
        data=report_text,
        file_name="classroom_analytics_report.txt",
        mime="text/plain"
    )