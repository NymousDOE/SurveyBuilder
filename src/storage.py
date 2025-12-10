"""
Storage management for Survey Builder Application

Handles in-memory storage with JSON persistence
"""

import json
import os
from typing import List, Optional, Dict, Any
from datetime import datetime

from src.models import (
    Survey,
    Question,
    TextQuestion,
    MultipleChoiceQuestion,
    ScaleQuestion,
    QuestionType,
    SurveyStatus
)


class SurveyStorage:
    """In-memory storage with JSON persistence"""
    
    def __init__(self, storage_path: str = "surveys_data.json"):
        self.storage_path = storage_path
        self.surveys: Dict[str, Survey] = {}
        self.load_from_file()
    
    def create_survey(self, title: str, description: str = "") -> Survey:
        """Create a new survey"""
        survey = Survey(title=title, description=description)
        self.surveys[survey.id] = survey
        self.save_to_file()
        return survey
    
    def get_survey(self, survey_id: str) -> Optional[Survey]:
        """Get a survey by ID"""
        return self.surveys.get(survey_id)
    
    def list_surveys(self) -> List[Survey]:
        """List all surveys"""
        return list(self.surveys.values())
    
    def delete_survey(self, survey_id: str) -> bool:
        """Delete a survey"""
        if survey_id in self.surveys:
            del self.surveys[survey_id]
            self.save_to_file()
            return True
        return False
    
    def add_question_to_survey(
        self,
        survey_id: str,
        question_type: str,
        text: str,
        **kwargs
    ) -> Question:
        """Add a question to a survey"""
        survey = self.get_survey(survey_id)
        if not survey:
            raise ValueError(f"Survey {survey_id} not found")
        
        # Create appropriate question type
        question = self._create_question(question_type, text, **kwargs)
        survey.add_question(question)
        self.save_to_file()
        return question
    
    def _create_question(
        self,
        question_type: str,
        text: str,
        **kwargs
    ) -> Question:
        """Factory method to create questions"""
        q_type = QuestionType(question_type)
        
        if q_type == QuestionType.TEXT:
            return TextQuestion(text=text)
        elif q_type == QuestionType.MULTIPLE_CHOICE:
            options = kwargs.get('options', [])
            return MultipleChoiceQuestion(text=text, options=options)
        elif q_type == QuestionType.SCALE:
            min_val = kwargs.get('min_value', 1)
            max_val = kwargs.get('max_value', 5)
            return ScaleQuestion(
                text=text,
                min_value=min_val,
                max_value=max_val
            )
        else:
            raise ValueError(f"Unknown question type: {question_type}")
    
    def save_to_file(self) -> None:
        """Persist surveys to JSON file"""
        data = {
            "surveys": [],
            "saved_at": datetime.utcnow().isoformat()
        }
        
        for survey in self.surveys.values():
            survey_data = {
                "id": survey.id,
                "title": survey.title,
                "description": survey.description,
                "status": survey.status.value,
                "created_at": survey.created_at.isoformat(),
                "questions": [],
                "responses": survey.responses
            }
            
            for question in survey.questions:
                q_data = {
                    "id": question.id,
                    "type": question.type.value,
                    "text": question.text
                }
                
                if isinstance(question, MultipleChoiceQuestion):
                    q_data["options"] = question.options
                elif isinstance(question, ScaleQuestion):
                    q_data["min_value"] = question.min_value
                    q_data["max_value"] = question.max_value
                
                survey_data["questions"].append(q_data)
            
            data["surveys"].append(survey_data)
        
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self) -> None:
        """Load surveys from JSON file"""
        if not os.path.exists(self.storage_path):
            return
        
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
            
            for survey_data in data.get("surveys", []):
                survey = Survey(
                    title=survey_data["title"],
                    description=survey_data["description"],
                    survey_id=survey_data["id"]
                )
                survey.status = SurveyStatus(survey_data["status"])
                survey.created_at = datetime.fromisoformat(
                    survey_data["created_at"]
                )
                survey.responses = survey_data.get("responses", [])
                
                # Restore questions
                for q_data in survey_data.get("questions", []):
                    question = self._restore_question(q_data)
                    survey.questions.append(question)
                
                self.surveys[survey.id] = survey
                
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error loading data: {e}")
            # Continue with empty storage if file is corrupted
    
    def _restore_question(self, q_data: Dict[str, Any]) -> Question:
        """Restore question from dictionary"""
        q_type = QuestionType(q_data["type"])
        
        if q_type == QuestionType.TEXT:
            return TextQuestion(
                text=q_data["text"],
                question_id=q_data["id"]
            )
        elif q_type == QuestionType.MULTIPLE_CHOICE:
            return MultipleChoiceQuestion(
                text=q_data["text"],
                options=q_data["options"],
                question_id=q_data["id"]
            )
        elif q_type == QuestionType.SCALE:
            return ScaleQuestion(
                text=q_data["text"],
                min_value=q_data["min_value"],
                max_value=q_data["max_value"],
                question_id=q_data["id"]
            )
        else:
            raise ValueError(f"Unknown question type: {q_data['type']}")


# Global storage instance
_storage = None


def get_storage() -> SurveyStorage:
    """Get the global storage instance"""
    global _storage
    if _storage is None:
        _storage = SurveyStorage()
    return _storage
