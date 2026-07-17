import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILLS = [
    "python","java","c++","html","css","javascript",
    "flask","django","sql","mysql","mongodb",
    "machine learning","deep learning","tensorflow",
    "pandas","numpy","git","github","aws","docker",
    "kubernetes","react","node","linux","rest api",
    "communication","teamwork","problem solving","api",
    "restful api","oop","object oriented programming",
    "data structures","algorithms","dsa","express",
    "bootstrap","tailwind","sqlite","postgresql",
    "firebase","azure","gcp","agile","jira","postman",
    "jwt",]

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9+# ]', ' ', text)
    return text


def calculate_similarity(resume_text, jd):

    docs = [
        clean_text(resume_text),
        clean_text(jd)
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1,2)
    )

    matrix = vectorizer.fit_transform(docs)

    score = cosine_similarity(
        matrix[0:1],
        matrix[1:2]
    )[0][0]

    score = score * 100

    # Prevent unrealistically low scores
    if score < 20:
        score += 20
    elif score < 40:
        score += 15

    return round(min(score,100),2)
def extract_skills(text):

    text = clean_text(text)

    found = []

    for skill in SKILLS:

        if skill in text:
            found.append(skill.title())

    return sorted(found)


def compare_skills(resume_text, jd):

    resume = set(extract_skills(resume_text))

    job = set(extract_skills(jd))

    matched = sorted(resume & job)

    missing = sorted(job - resume)

    return matched, missing


def resume_strength(score):

    if score >= 80:
        return "Excellent"

    elif score >= 60:
        return "Good"

    elif score >= 40:
        return "Average"

    return "Needs Improvement"
def ats_breakdown(resume_text, job_description):

    resume = resume_text.lower()

    matched, missing = compare_skills(resume_text, job_description)

    total = len(matched) + len(missing)

    if total:
        skills_score = round((len(matched) / total) * 100, 2)
    else:
        skills_score = 0

    education = 100 if any(word in resume for word in [
        "b.tech",
        "btech",
        "bachelor",
        "degree",
        "university",
        "college"
    ]) else 40

    projects = 100 if any(word in resume for word in [
        "project",
        "projects"
    ]) else 40

    experience = 100 if any(word in resume for word in [
        "experience",
        "internship",
        "worked"
    ]) else 50

    overall = round(
        (
            skills_score +
            education +
            projects +
            experience
        ) / 4,
        2
    )

    return {
        "overall": overall,
        "skills": skills_score,
        "education": education,
        "projects": projects,
        "experience": experience
    }
def analyze_sections(resume_text):

    text = resume_text.lower()

    sections = {
        "Contact Information": any(word in text for word in [
            "@", "phone", "mobile", "contact"
        ]),

        "Education": any(word in text for word in [
            "education", "b.tech", "bachelor",
            "college", "university"
        ]),

        "Skills": any(word in text for word in [
            "skills", "python", "java",
            "html", "css"
        ]),

        "Projects": any(word in text for word in [
            "project", "projects"
        ]),

        "Experience": any(word in text for word in [
            "experience", "internship", "worked"
        ]),

        "Certifications": any(word in text for word in [
            "certificate", "certification"
        ]),

        "Achievements": any(word in text for word in [
            "achievement", "award", "winner"
        ])
    }

    return sections
def resume_feedback(score, matched, missing):

    strengths = []
    weaknesses = []
    recommendations = []

    if score >= 80:
        strengths.append("High similarity with the job description.")
    elif score >= 60:
        strengths.append("Moderate similarity with the job description.")
    else:
        weaknesses.append("Resume has a low similarity with the job description.")

    if len(matched) >= 5:
        strengths.append("Strong technical skill coverage.")
    else:
        weaknesses.append("Limited matching technical skills.")

    if len(missing) > 0:
        weaknesses.append("Some required skills are missing.")
        recommendations.append("Add the missing skills if you have practical experience.")

    recommendations.append("Include measurable project outcomes.")
    recommendations.append("Keep your resume to one page.")
    recommendations.append("Use action verbs such as Developed, Built, Designed.")

    return strengths, weaknesses, recommendations