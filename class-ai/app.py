import whisper


def analyze_classroom_audio(audio_file):
    model = whisper.load_model("base")
    # Raw (original language)
    result_raw = model.transcribe(audio_file)

    # Translated (English)
    result_en = model.transcribe(audio_file, task="translate")

    raw_text = result_raw["text"]
    text = result_en["text"]

    clean_text = text.replace("?", ".")
    sentences = [s.strip() for s in clean_text.split(".") if s.strip()]

    questions = text.count("?")

    teacher_keywords = [
    "what", "why", "how", "tell", "explain",
    "answer", "class", "listen", "say",
    "come here", "repeat", "speak"
   
    ]

    student_keywords = [
    "yes", "no", "my name is", "present",
    "here", "sir", "maam"
    
    ]

    teacher_words = 0
    student_words = 0
    teacher_sentences = 0
    student_sentences = 0

    for s in sentences:
        words = len(s.split())
        s_lower = s.lower()

        speaker = "teacher"

        if any(word in s_lower for word in teacher_keywords):
            speaker = "teacher"
        elif any(word in s_lower for word in student_keywords):
            speaker = "student"
        elif words <= 3:
            speaker = "student"

        if speaker == "teacher":
            teacher_words += words
            teacher_sentences += 1
        else:
            student_words += words
            student_sentences += 1

    words_per_second = 2.5
    teacher_time = teacher_words / words_per_second
    student_time = student_words / words_per_second

    total_time = teacher_time + student_time
    if total_time == 0:
        total_time = 1

    teacher_ratio = teacher_time / total_time
    student_ratio = student_time / total_time

    segments = result_raw.get("segments", [])

    silence_time = 0
    for i in range(1, len(segments)):
        prev_end = segments[i - 1]["end"]
        curr_start = segments[i]["start"]
        gap = curr_start - prev_end
        if gap > 0:
            silence_time += gap

    total_audio_time = segments[-1]["end"] if segments else 1
    silence_ratio = silence_time / total_audio_time if total_audio_time > 0 else 0

    student_response_count = student_sentences
    teacher_dominance = teacher_time / total_time
    student_participation = student_response_count / (
        teacher_sentences + student_sentences if (teacher_sentences + student_sentences) > 0 else 1
    )
    interaction_count = teacher_sentences + student_sentences

    total_words = teacher_words + student_words
    if total_words == 0:
        total_words = 1

    teacher_speech_percent = (teacher_words / total_words) * 100
    student_speech_percent = (student_words / total_words) * 100
    language_map = {
    "hi": "Hindi",
    "en": "English",
    "ta": "Tamil",
    "te": "Telugu",
    "ml": "Malayalam"
}

    detected_lang = result_raw.get("language")
    language_full = language_map.get(detected_lang, detected_lang)

    return {
        "raw_transcript": raw_text,
        "language": language_full,
        "transcript": text,
        "teacher_words": teacher_words,
        "student_words": student_words,
        "teacher_speech_percent": teacher_speech_percent,
        "student_speech_percent": student_speech_percent,
        "teacher_time": teacher_time,
        "student_time": student_time,
        "questions": questions,
        "student_responses": student_response_count,
        "teacher_dominance": teacher_dominance,
        "student_participation": student_participation,
        "interaction_count": interaction_count,
        "silence_time": silence_time,
        "silence_ratio": silence_ratio,
    }


if __name__ == "__main__":
    output = analyze_classroom_audio("audio2.mp3")

    print("\nDetected language:", output["language"])
    print("\nTranscript:\n")
    print(output["transcript"])

    print("\n--- Teacher vs Student Speech ---")
    print(f'Teacher speech: {output["teacher_words"]} words ({output["teacher_speech_percent"]:.2f}%)')
    print(f'Student speech: {output["student_words"]} words ({output["student_speech_percent"]:.2f}%)')

    print("\n--- Classroom Analysis ---")
    print(f'Teacher talk time: {output["teacher_time"]:.2f} sec')
    print(f'Student talk time: {output["student_time"]:.2f} sec')
    print(f'Questions asked: {output["questions"]}')
    print(f'Student responses: {output["student_responses"]}')

    print("\n--- Engagement Metrics ---")
    print(f'Teacher Dominance Ratio: {output["teacher_dominance"]:.2f}')
    print(f'Student Participation Indicator: {output["student_participation"]:.2f}')
    print(f'Interaction Count: {output["interaction_count"]}')

    print("\n--- Silence Analysis ---")
    print(f'Silence duration: {output["silence_time"]:.2f} sec')
    print(f'Silence ratio: {output["silence_ratio"]:.2f}')