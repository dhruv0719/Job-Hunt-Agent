# app/ingestion/parsers/resume_parser.py

import re
from typing import List, Dict
from loader.resume_loader import ResumeLoader
from app.model.resume import Resume, PersonalInformation


class ResumeParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.loader = ResumeLoader(file_path)
        self.links = []

    def parse(self) -> Resume:
        """
        Parse the resume file and extract relevant information.
        
        Returns:
            Resume: An instance of Resume containing extracted information.
        """
        resume_text = self.loader.load_resume()
        if not resume_text:
            print("Failed to load resume text.")
            return None

        links = self.loader.extract_url()
        parsed_resume = self.parse_resume(resume_text)
        if parsed_resume:
            parsed_resume.links = links
            return parsed_resume
        else:
            print("Failed to parse resume.")
            return None
        
    def parse_resume(self, resume_text: str) -> Resume:
        """
        Parse the resume text and extract relevant information.

        Args:
            resume_text (str): The text content of the resume.

        Returns:
            Resume: An instance of Resume containing extracted information.
        """
        try:

            # Extract name, email, phone number
             

            # Extract links from the resume text
            links = ResumeLoader.extract_url(resume_text)
            
            return Resume(
                personal_information=self._personal_information(resume_text),
                skills=["Extracted Skill 1", "Extracted Skill 2"],
                experience=[{"company": "Company A", "role": "Role A"}],
                education=[{"institution": "University A", "degree": "Degree A"}],
                certifications=["Certification A"],
                projects=[{"project_name": "Project A", "description": "Description A"}],
                languages=["Language A"],
                links=links,
                miscellaneous={"key": "value"}
            )

        except Exception as e:
            print(f"Error parsing resume: {e}")
            return None
        
    def _personal_information(self, resume_text: str) -> PersonalInformation:
        """
        Extract personal information such as name, email, and phone number from the resume text.

        Args:
            resume_text (str): The text content of the resume.
        
        Returns:
            PersonalInformation: An instance of PersonalInformation containing extracted personal information.
        """

        return PersonalInformation(
            name=self._extract_name(resume_text),
            email=self._extract_email(resume_text),
            phone_number=self._extract_phone_number(resume_text)
        )
        
    def _extract_name(self, resume_text: str) -> str:
        name = input("Please enter the name extracted from the resume: ")
        return name.strip() if name else None

    def _extract_email(self, resume_text: str) -> str:
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(email_pattern, resume_text)
        return match.group(0) if match else None

    def _extract_phone_number(self, resume_text: str) -> str:
        phone_pattern = r'\+?\d[\d -]{8,}\d'
        match = re.search(phone_pattern, resume_text)
        return match.group(0) if match else None   

    def _extract_session(self, resume_text: str) -> Dict[str, str]:
        """
        Extract session information from the resume text.

        Args:
            resume_text (str): The text content of the resume.
        
        Returns:
            Dict[str, str]: A dictionary containing session information.
        """
        pass
