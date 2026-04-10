# Classroom Voice Analytics MVP

## Overview

This project is a prototype for classroom voice analytics. It processes classroom audio and generates:

- original transcript
- translated transcript in English
- teacher vs student speech estimates
- talk-time comparison
- question count
- student response count
- silence duration
- engagement metrics
- short classroom summary

The goal is to demonstrate a simple AI-powered classroom analytics workflow.

---

## Approach

The system takes a classroom audio file as input and processes it in the following stages:

1. **Speech-to-text**
   - OpenAI Whisper is used to transcribe the uploaded audio.
   - The system also generates an English translation of the transcript for readability.

2. **Text processing**
   - The translated transcript is cleaned and split into sentences.
   - Questions are estimated using question marks in the transcript.

3. **Teacher vs Student estimation**
   - A heuristic-based approach is used.
   - Teacher and student speech are approximated using keyword-based rules and sentence-length patterns.

4. **Metric calculation**
   - Teacher and student word counts are estimated from classified sentences.
   - Talk time is estimated by converting word counts into seconds using an average speaking rate.

5. **Silence detection**
   - Silence duration is estimated using timestamp gaps between Whisper speech segments.

6. **Demo interface**
   - A Streamlit app is used to upload audio and display transcripts, metrics, and summary.

---

## How Metrics Were Calculated

### Teacher vs Student Speech

Estimated using sentence classification and total word counts:

- Teacher speech = total words in teacher-classified sentences
- Student speech = total words in student-classified sentences

### Teacher Talk Time

Estimated using:

- `teacher_time = teacher_words / 2.5`

### Student Talk Time

Estimated using:

- `student_time = student_words / 2.5`

Assumption:

- average speaking rate ≈ 2.5 words per second

### Questions Asked

Estimated using:

- number of `?` symbols in the translated transcript

### Student Response Count

Estimated using:

- number of student-classified sentences

### Teacher Dominance Ratio

Calculated as:

- `teacher_time / (teacher_time + student_time)`

### Student Participation Indicator

Calculated as:

- `student_responses / total_interactions`

### Interaction Count

Calculated as:

- `teacher_sentences + student_sentences`

### Silence Duration

Calculated using gaps between consecutive Whisper segments.

---

## Tools / Models Used

- Python
- Streamlit
- OpenAI Whisper
- Torch
- ffmpeg-python

---

## Assumptions

- Approximate transcription is acceptable for this MVP.
- The translated English transcript is used for cleaner downstream analysis.
- Teacher/student speech is estimated heuristically, not through full speaker diarization.
- Speaking rate is approximated as 2.5 words per second.
- Silence is approximated from gaps between detected speech segments.

---

## Limitations

- Classroom audio may contain noise, overlapping speech, and code-mixed language.
- Whisper transcription may not always be perfectly accurate.
- Teacher/student classification is heuristic-based and may misclassify some lines.
- Speaker diarization is not used in this prototype.
- Metrics are approximate and intended for MVP demonstration only.

---

## Instrucitons

### Installation

Install dependencies:

````bash
pip install -r requirements.txt

Run the Application
Start the Streamlit app using:

```bash
streamlit run streamlit_app.py


### Usage Instructions

Upload a classroom audio file (mp3 / wav / m4a)
Wait for the system to process the audio
⏳ Note: Processing may take some time depending on audio length and system performance
The output may appear gradually
View the results:
Detected language
Original transcript
Translated transcript
Teacher vs student speech analysis
Engagement metrics
Silence analysis
Classroom summary
Click the Download Report button to save the results

---

## Deployment

This prototype is currently designed to run locally.

Online deployment can be done using platforms such as:
- Streamlit Cloud
- Hugging Face Spaces
- Render

However, local execution is recommended for this MVP because the Whisper model can be computationally heavy and free hosting platforms may have memory or performance limitations.

To run locally:

```bash
streamlit run streamlit_app.py


---
## Future Improvements

- Integrate **speaker diarization** to identify different speakers based on voice instead of relying only on transcript-based heuristics

- Speaker diarization helps determine *who spoke when* in an audio recording, enabling more accurate separation of teacher and student speech

- A possible improved pipeline:
  - First segment audio by speaker (voice-based separation)
  - Then identify the teacher based on characteristics such as:
    - longest speaking duration
    - higher number of questions or instructions
  - Treat remaining speakers as students
  - Compute metrics based on speaker groups

- Tools that can be used for this:
  - **WhisperX** (transcription + alignment + diarization)
  - **pyannote.audio** (speaker diarization pipelines)
  - **NVIDIA NeMo** (advanced diarization and speech models)

- This approach is more robust than keyword-based classification, especially in cases where:
  - teachers use student-like keywords
  - students repeat teacher phrases
  - transcripts contain noise or mixed language

- Improve handling of noisy classroom audio, overlapping speech, and background disturbances

- Improve robustness for unclear, distorted, or unusual voice patterns in classroom recordings

- Use stronger multilingual or Hindi-focused speech recognition models for better transcription accuracy

- Enhance teacher vs student classification using both voice features and text-based cues

- Add better question and response detection using NLP techniques instead of simple heuristics

- Extend support for multiple Indian languages with improved accuracy

- Add visualizations such as charts and dashboards

- Enable real-time or near real-time classroom audio processing

- Improve report generation with downloadable PDF summaries
````
