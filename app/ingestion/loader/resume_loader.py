# app/ingestion/loader/resume_loader.py
import pymupdf
import re
from typing import List

class ResumeLoader:
    def __init__(self, file_path):
        self.file_path = file_path 
        self.link = []

    def load_resume(self) -> str:
        """Load the resume from the specified file path."""
        try: 
            with pymupdf.open(self.file_path) as doc:
                return "\n".join(page.get_text() for page in doc)

        except Exception as e:
            print(f"Error loading resume: {e}")
            return None
            
    def extract_url(self) -> List[str]:
        """Extract URLs from the loaded resume text."""
        for page in pymupdf.open(self.file_path):
            # Clickable links
            for link in page.get_links():
                if "uri" in link:
                    self.link.append(link["uri"])

            # URLs written as plain text
            text = page.get_text()
            self.link.extend(re.findall(r'(https?://\S+)', text))
        
        return self.link
    
    
if __name__ == "__main__":
    # Example usage
    loader = ResumeLoader("D:/Dhruv's_Resume.pdf")
    resume_text = loader.load_resume()
    resume_links = loader.extract_url()

    if resume_text:
        print(resume_text)
        print("Extracted URLs:", resume_links)