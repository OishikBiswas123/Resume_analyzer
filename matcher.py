from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


SKILL_ALIASES = {
    "ml": "machine learning",
    "dl": "deep learning",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "tf": "tensorflow",
    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "js": "javascript",
    "py": "python",
    "HTML": "html",
    "CSS": "css",
    "react": "react.js",
    "angular": "angular.js",
    "vue": "vue.js",
    "gen ai": "generative AI",
    "rag": "retrieval augmented generation"
    }


def normalize_skills(skills):
    normalized_skills = []

    for skill in skills:
        skill = skill.lower().strip()

        if skill in SKILL_ALIASES:
            skill = SKILL_ALIASES[skill]

        normalized_skills.append(skill)

    return normalized_skills


def calculate_skill_match(resume_skills, jd_skills, threshold=0.60):
    if not jd_skills:
        return 0, [], []

    if not resume_skills:
        return 0, [], jd_skills

    resume_skills = normalize_skills(resume_skills)
    jd_skills = normalize_skills(jd_skills)

    resume_embeddings = embedding_model.encode(resume_skills)
    jd_embeddings = embedding_model.encode(jd_skills)

    matched_skills = []
    missing_skills = []

    for i, jd_skill in enumerate(jd_skills):
        similarities = cosine_similarity(
            [jd_embeddings[i]],
            resume_embeddings
        )[0]

        best_match_index = similarities.argmax()
        best_score = similarities[best_match_index]
        best_resume_skill = resume_skills[best_match_index]

        if best_score >= threshold:
            matched_skills.append(
                f"{jd_skill} ↔ {best_resume_skill}"
            )
        else:
            missing_skills.append(jd_skill)

    skill_score = (len(matched_skills) / len(jd_skills)) * 100

    return round(float(skill_score), 2), matched_skills, missing_skills


def calculate_semantic_similarity(resume_text, job_description):
    embeddings = embedding_model.encode([resume_text, job_description])

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(float(similarity * 100), 2)


def calculate_final_score(skill_score, semantic_score):
    final_score = (0.7 * skill_score) + (0.3 * semantic_score)
    return round(float(final_score), 2)