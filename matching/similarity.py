import numpy as np
from models.embeddings import EmbeddingModel, calculate_similarity

class JobMatcher:
    def __init__(self):
        self.model = EmbeddingModel()

    def match(self, cv_text, job_description):
        """
        Compare le CV et l'offre d'emploi.
        """
        cv_embedding = self.model.get_embeddings(cv_text)
        job_embedding = self.model.get_embeddings(job_description)
        
        score = calculate_similarity(cv_embedding, job_embedding)
        return round(score * 100, 2)

    def extract_keywords_match(self, cv_text, job_text):
        """
        Analyse simplifiée des mots-clés pour le feedback (Skills).
        Inclut des compétences spécifiques pour l'IA, la Data, le Cloud et la Cybersécurité.
        """
        # Compétences générales
        general_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js',
            'sql', 'nosql', 'mongodb', 'git', 'scrum', 'agile', 'project management',
            'communication', 'english', 'french', 'php', 'c++', 'c#', 'typescript'
        ]

        # Compétences IA
        ai_skills = [
            'machine learning', 'deep learning', 'nlp', 'computer vision', 'reinforcement learning',
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'r', 'matlab', 'openai', 'llm',
            'generative ai', 'prompt engineering', 'mlops', 'data labeling', 'model deployment'
        ]

        # Compétences Data
        data_skills = [
            'data science', 'data analysis', 'data engineering', 'big data', 'data visualization',
            'pandas', 'numpy', 'spark', 'hadoop', 'tableau', 'power bi', 'excel', 'etl',
            'data warehousing', 'sql', 'nosql', 'data governance', 'data mining', 'statistics'
        ]

        # Compétences Cloud
        cloud_skills = [
            'aws', 'azure', 'google cloud platform', 'gcp', 'docker', 'kubernetes', 'terraform',
            'ansible', 'devops', 'ci/cd', 'cloud security', 'serverless', 'lambda', 'azure functions',
            'ec2', 's3', 'vpc', 'cloudformation', 'containerization', 'virtualization'
        ]

        # Compétences Cybersécurité
        cyber_skills = [
            'cybersecurity', 'network security', 'information security', 'ethical hacking', 'penetration testing',
            'vulnerability assessment', 'incident response', 'security operations', 'soc', 'siem',
            'firewall', 'vpn', 'cryptography', 'malware analysis', 'forensics', 'gdpr', 'iso 27001',
            'risk management', 'identity and access management', 'iam', 'endpoint security'
        ]
        
        # Combiner toutes les compétences
        all_common_skills = list(set(general_skills + ai_skills + data_skills + cloud_skills + cyber_skills))
        
        cv_text = cv_text.lower()
        job_text = job_text.lower()
        
        matched_skills = [skill for skill in all_common_skills if skill in cv_text and skill in job_text]
        missing_skills = [skill for skill in all_common_skills if skill in job_text and skill not in cv_text]
        
        return matched_skills, missing_skills
