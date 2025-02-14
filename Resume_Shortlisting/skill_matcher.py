import spacy
from .utils import load_skill_patterns

class SkillMatcher:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.skill_patterns = load_skill_patterns()
    
    def match_skills(self, resume_text, job_description):
        """Match skills between resume and job description"""
        resume_skills = self._extract_skills(resume_text)
        required_skills = self._extract_skills(job_description)
        
        if required_skills:
            skill_match = len(set(resume_skills) & set(required_skills)) / len(required_skills)
        else:
            skill_match = 0
            
        return {
            'skill_match': skill_match,
            'matched_skills': list(set(resume_skills) & set(required_skills)),
            'missing_skills': list(set(required_skills) - set(resume_skills))
        }
    
    def _extract_skills(self, text):
        """Extract skills from text"""
        doc = self.nlp(text.lower())
        skills = []
        
        for skill in self.skill_patterns:
            if skill in text.lower():
                skills.append(skill)
                
        return list(set(skills))
    
    def extract_experience(self, text):
        """Extract years of experience"""
        doc = self.nlp(text)
        experience = 0
        
        for ent in doc.ents:
            if ent.label_ == "DATE" and "year" in ent.text.lower():
                try:
                    num = int(''.join(filter(str.isdigit, ent.text)))
                    if num < 50:  # Reasonable experience limit
                        experience = max(experience, num)
                except ValueError:
                    continue
                    
        return experience