import re
from typing import Dict


class ResumeScorer:

    def __init__(self, weights=None):
        # Default weights
        self.weights = weights or {
            "semantic": 0.5,
            "skills": 0.3,
            "experience": 0.2
        }

    # -------------------------
    # SKILL MATCHING
    # -------------------------
    def skill_match_score(self, resume_skills, jd_text):
        jd_text = jd_text.lower()

        if not resume_skills:
            return 0.0

        # Create skill variations for better matching
        skill_variations = {}
        for skill in resume_skills:
            skill_variations[skill] = [
                skill,  # exact match
                skill.replace(' ', ''),  # no spaces
                skill.replace(' ', '-'),  # hyphenated
                skill.replace('++', 'pp'),  # c++ -> cpp
            ]
            if skill == 'c++':
                skill_variations[skill].extend(['cpp', 'c plus plus'])

        matched = 0
        for skill in resume_skills:
            # Check all variations
            skill_matched = False
            for variation in skill_variations[skill]:
                if variation in jd_text:
                    skill_matched = True
                    break
            if skill_matched:
                matched += 1

        return matched / len(resume_skills)

    # -------------------------
    # EXPERIENCE MATCH (Heuristic)
    # -------------------------
    def experience_score(self, resume_text, jd_text):
        """
        Extract years of experience and compare
        """
        def extract_years(text):
            # More comprehensive patterns for experience
            patterns = [
                r'(\d+)\s+years?\s+(?:of\s+)?experience',
                r'(\d+)\s+years?\s+in\s+',
                r'experience\s+(?:of\s+)?(\d+)\s+years?',
                r'(\d+)\+?\s*years?',
            ]

            all_matches = []
            for pattern in patterns:
                matches = re.findall(pattern, text.lower())
                all_matches.extend([int(m) for m in matches])

            return max(all_matches, default=0) if all_matches else 0

        resume_years = extract_years(resume_text)
        jd_years = extract_years(jd_text)

        if jd_years == 0:
            return 1.0  # no constraint

        # Give partial credit for close matches
        if resume_years >= jd_years:
            return 1.0
        elif resume_years >= jd_years * 0.8:  # within 80%
            return 0.8
        elif resume_years >= jd_years * 0.5:  # within 50%
            return 0.5
        else:
            return resume_years / jd_years

    # -------------------------
    # FINAL SCORE
    # -------------------------
    def compute_score(
        self,
        semantic_score: float,
        resume_data: Dict,
        jd_text: str
    ) -> Dict:

        skill_score = self.skill_match_score(
            resume_data.get("skills", []),
            jd_text
        )

        experience_score = self.experience_score(
            resume_data.get("cleaned_text", ""),
            jd_text
        )

        final_score = (
            self.weights["semantic"] * semantic_score +
            self.weights["skills"] * skill_score +
            self.weights["experience"] * experience_score
        )

        # Normalize to 0–100
        final_score_100 = int(final_score * 100)

        decision = "Fit" if final_score_100 >= 50 else "Not Fit"

        reason = self.generate_reason(
            semantic_score,
            skill_score,
            experience_score
        )

        return {
            "final_score": final_score_100,
            "semantic_score": round(semantic_score, 3),
            "skill_score": round(skill_score, 3),
            "experience_score": round(experience_score, 3),
            "decision": decision,
            "reason": reason
        }

    # -------------------------
    # EXPLANATION GENERATION
    # -------------------------
    def generate_reason(self, semantic, skills, experience):

        reasons = []

        if semantic > 0.75:
            reasons.append("Strong overall relevance to job description")
        elif semantic < 0.4:
            reasons.append("Low relevance to job description")

        if skills > 0.7:
            reasons.append("Good skill match")
        elif skills < 0.3:
            reasons.append("Insufficient skill match")

        if experience > 0.7:
            reasons.append("Satisfies experience requirements")
        elif experience < 0.4:
            reasons.append("Lacks required experience")

        return "; ".join(reasons)