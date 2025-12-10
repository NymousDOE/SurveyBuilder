from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional
import uuid


class SurveyStatus(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"


class QuestionType(Enum):
    TEXT = "text"
    MULTIPLE_CHOICE = "multiple_choice"
    SCALE = "scale"


class Question:
    def __init__(
        self, question_type: QuestionType, text: str, question_id: Optional[str] = None
    ):
        self.id = question_id or str(uuid.uuid4())
        self.type = question_type
        self.text = text

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "type": self.type.value, "text": self.text}

    def validate_answer(self, answer: Any) -> bool:
        raise NotImplementedError


class TextQuestion(Question):
    def __init__(self, text: str, question_id: Optional[str] = None):
        super().__init__(QuestionType.TEXT, text, question_id)

    def validate_answer(self, answer: Any) -> bool:
        return isinstance(answer, str) and len(answer.strip()) > 0


class MultipleChoiceQuestion(Question):
    def __init__(
        self, text: str, options: List[str], question_id: Optional[str] = None
    ):
        super().__init__(QuestionType.MULTIPLE_CHOICE, text, question_id)
        if len(options) < 2:
            raise ValueError("Multiple choice question needs at least 2 options")
        self.options = options

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["options"] = self.options
        return data

    def validate_answer(self, answer: Any) -> bool:
        return answer in self.options


class ScaleQuestion(Question):
    def __init__(
        self,
        text: str,
        min_value: int = 1,
        max_value: int = 5,
        question_id: Optional[str] = None,
    ):
        super().__init__(QuestionType.SCALE, text, question_id)
        if min_value >= max_value:
            raise ValueError("min_value must be less than max_value")
        self.min_value = min_value
        self.max_value = max_value

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["min_value"] = self.min_value
        data["max_value"] = self.max_value
        return data

    def validate_answer(self, answer: Any) -> bool:
        return isinstance(answer, int) and self.min_value <= answer <= self.max_value


class Survey:
    def __init__(
        self, title: str, description: str = "", survey_id: Optional[str] = None
    ):
        self.id = survey_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.questions: List[Question] = []
        self.status = SurveyStatus.DRAFT
        self.created_at = datetime.utcnow()
        self.responses: List[Dict[str, Any]] = []

    def add_question(self, question: Question) -> None:
        if self.status != SurveyStatus.DRAFT:
            raise ValueError("Cannot modify published survey")
        self.questions.append(question)

    def remove_question(self, question_id: str) -> bool:
        if self.status != SurveyStatus.DRAFT:
            raise ValueError("Cannot modify published survey")

        for i, q in enumerate(self.questions):
            if q.id == question_id:
                self.questions.pop(i)
                return True
        return False

    def publish(self) -> None:
        if len(self.questions) == 0:
            raise ValueError("Cannot publish survey without questions")
        self.status = SurveyStatus.PUBLISHED

    def add_response(self, responses: Dict[str, Any]) -> str:
        if self.status != SurveyStatus.PUBLISHED:
            raise ValueError("Survey must be published to accept responses")

        for question in self.questions:
            if question.id not in responses:
                raise ValueError(f"Missing answer for question {question.id}")
            if not question.validate_answer(responses[question.id]):
                raise ValueError(f"Invalid answer for question {question.id}")

        response_id = str(uuid.uuid4())
        response_data = {
            "id": response_id,
            "timestamp": datetime.utcnow().isoformat(),
            "answers": responses,
        }
        self.responses.append(response_data)
        return response_id

    def get_results(self) -> Dict[str, Any]:
        results = {
            "survey_id": self.id,
            "title": self.title,
            "response_count": len(self.responses),
            "questions": [],
        }

        for question in self.questions:
            q_results = {
                "question_id": question.id,
                "text": question.text,
                "type": question.type.value,
            }

            answers = [r["answers"][question.id] for r in self.responses]

            if question.type == QuestionType.TEXT:
                q_results["answer_count"] = len(answers)

            elif question.type == QuestionType.MULTIPLE_CHOICE:
                distribution = {}
                for opt in question.options:
                    count = answers.count(opt)
                    distribution[opt] = {
                        "count": count,
                        "percentage": (
                            round(count / len(answers) * 100, 2) if answers else 0
                        ),
                    }
                q_results["distribution"] = distribution

            elif question.type == QuestionType.SCALE:
                if answers:
                    q_results["average"] = round(sum(answers) / len(answers), 2)
                    q_results["min"] = min(answers)
                    q_results["max"] = max(answers)
                else:
                    q_results["average"] = 0
                    q_results["min"] = 0
                    q_results["max"] = 0

            results["questions"].append(q_results)

        return results

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "question_count": len(self.questions),
            "response_count": len(self.responses),
            "created_at": self.created_at.isoformat(),
            "questions": [q.to_dict() for q in self.questions],
        }
