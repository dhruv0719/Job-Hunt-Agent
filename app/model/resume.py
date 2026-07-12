# app/model/resume.py

from typing import List, Dict
from dataclasses import dataclass, field


@dataclass
class Experience:
    company: str
    role: str
    duration: str
    description: str

@dataclass
class Education:
    institution: str
    degree: str
    field_of_study: str
    start_year: str
    end_year: str

@dataclass
class Project:
    title: str
    description: str
    technologies: List[str]
    link: str

@dataclass
class PersonalInformation:
    name: str
    email: str
    phone_number: str

@dataclass
class Resume:
    personal_information: PersonalInformation
    skills: List[str] = field(default_factory=list)
    experience: List[Experience]
    education: List[Education]
    certifications: List[str]
    projects: List[Project]
    languages: List[str] = field(default_factory=list)
    links: List[str]
    miscellaneous: Dict[str, str]