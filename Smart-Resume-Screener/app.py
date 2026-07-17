from flask import Flask, render_template, request
import os

from resume_parser import extract_text
from utils import (
    calculate_similarity,
    compare_skills,
    resume_strength,
    ats_breakdown,
    analyze_sections,
    resume_feedback
)
from report_generator import generate_report

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    if "resume" not in request.files:
        return "No resume uploaded."

    file = request.files["resume"]

    if file.filename == "":
        return "Please select a PDF file."

    job_description = request.form["job_description"]

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    # -----------------------------
    # Extract Resume Text
    # -----------------------------
    resume_text = extract_text(filepath)

    # -----------------------------
    # Cosine Similarity Score
    # -----------------------------
    cosine_score = calculate_similarity(
        resume_text,
        job_description
    )

    # -----------------------------
    # Skill Comparison
    # -----------------------------
    matched, missing = compare_skills(
        resume_text,
        job_description
    )

    total_skills = len(matched) + len(missing)

    if total_skills > 0:
        keyword_score = (len(matched) / total_skills) * 100
    else:
        keyword_score = 0

    # -----------------------------
    # ATS Breakdown
    # -----------------------------
    breakdown = ats_breakdown(
        resume_text,
        job_description
    )

    ats_score = sum(breakdown.values()) / len(breakdown)

    # -----------------------------
    # Final ATS Score
    # -----------------------------
    score = round(
        (cosine_score * 0.4) +
        (keyword_score * 0.4) +
        (ats_score * 0.2),
        2
    )

    # -----------------------------
    # Resume Strength
    # -----------------------------
    strength = resume_strength(score)

    # -----------------------------
    # Resume Sections
    # -----------------------------
    sections = analyze_sections(resume_text)

    # -----------------------------
    # Feedback
    # -----------------------------
    strengths, weaknesses, recommendations = resume_feedback(
        score,
        matched,
        missing
    )

    # -----------------------------
    # Suggestions
    # -----------------------------
    suggestions = []

    if score < 60:
        suggestions.append(
            "Increase the relevance of your resume by adding keywords from the job description."
        )

    if missing:
        suggestions.append(
            "Include the missing skills if you have practical experience."
        )

    suggestions.append(
        "Mention projects related to the required technologies."
    )

    suggestions.append(
        "Keep your resume concise and well structured."
    )

    # -----------------------------
    # Generate PDF Report
    # -----------------------------
    report_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "resume_report.pdf"
    )

    generate_report(
        report_path,
        score,
        strength,
        matched,
        missing,
        suggestions
    )

    # -----------------------------
    # Render Result Page
    # -----------------------------
    return render_template(
        "result.html",
        score=score,
        strength=strength,
        matched=matched,
        missing=missing,
        suggestions=suggestions,
        report_file="uploads/resume_report.pdf",
        breakdown=breakdown,
        sections=sections,
        strengths=strengths,
        weaknesses=weaknesses,
        recommendations=recommendations
    )


if __name__ == "__main__":
    app.run(debug=True)