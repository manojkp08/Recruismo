from .skill_matcher import SkillMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ResumeScreener:
    def __init__(self):
        self.skill_matcher = SkillMatcher()
        self.vectorizer = TfidfVectorizer()
    
    def score_resume(self, resume_text, job_description):
        """Score a resume against a job description"""
        # Get skill matches
        skill_score = self.skill_matcher.match_skills(resume_text, job_description)
        
        # Calculate text similarity
        try:
            tfidf_matrix = self.vectorizer.fit_transform([resume_text, job_description])
            text_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        except:
            text_similarity = 0
        
        # Get experience
        experience = self.skill_matcher.extract_experience(resume_text)
        
        return {
            'skill_match': skill_score['skill_match'] * 100,
            'text_similarity': text_similarity * 100,
            'experience_years': experience,
            'matched_skills': skill_score['matched_skills'],
            'missing_skills': skill_score['missing_skills'],
            'total_score': (skill_score['skill_match'] * 0.5 + text_similarity * 0.3 + min(experience/10, 1) * 0.2) * 100
        }