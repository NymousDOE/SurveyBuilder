import pytest
from datetime import datetime

from src.models import (
    Survey,
    TextQuestion,
    MultipleChoiceQuestion,
    ScaleQuestion,
    SurveyStatus,
    QuestionType
)

class TestTextQuestion:
    def test_create_text_question(self):
        q = TextQuestion("What is your name?")
        assert q.type == QuestionType.TEXT
        assert q.text == "What is your name?"
        assert q.id is not None

    def test_validate_valid_answer(self):
        q = TextQuestion("What is your name?")
        assert q.validate_answer("John Doe") is True

    def test_validate_empty_answer(self):
        q = TextQuestion("What is your name?")
        assert q.validate_answer("") is False
        assert q.validate_answer("   ") is False

    def test_validate_non_string(self):
        q = TextQuestion("What is your name?")
        assert q.validate_answer(123) is False

class TestMultipleChoiceQuestion:
    def test_create_multiple_choice_question(self):
        q = MultipleChoiceQuestion(
            "Choose your color",
            ["Red", "Blue", "Green"]
        )
        assert q.type == QuestionType.MULTIPLE_CHOICE
        assert len(q.options) == 3

    def test_too_few_options(self):
        with pytest.raises(ValueError):
            MultipleChoiceQuestion("Choose", ["Only one"])

    def test_validate_valid_answer(self):
        q = MultipleChoiceQuestion(
            "Choose your color",
            ["Red", "Blue", "Green"]
        )
        assert q.validate_answer("Red") is True
        assert q.validate_answer("Blue") is True

    def test_validate_invalid_answer(self):
        q = MultipleChoiceQuestion(
            "Choose your color",
            ["Red", "Blue", "Green"]
        )
        assert q.validate_answer("Yellow") is False

class TestScaleQuestion:
    def test_create_scale_question(self):
        q = ScaleQuestion("Rate our service", min_value=1, max_value=5)
        assert q.type == QuestionType.SCALE
        assert q.min_value == 1
        assert q.max_value == 5

    def test_invalid_range(self):
        with pytest.raises(ValueError):
            ScaleQuestion("Rate", min_value=5, max_value=1)

    def test_validate_valid_answer(self):
        q = ScaleQuestion("Rate", min_value=1, max_value=5)
        assert q.validate_answer(1) is True
        assert q.validate_answer(3) is True
        assert q.validate_answer(5) is True

    def test_validate_out_of_range(self):
        q = ScaleQuestion("Rate", min_value=1, max_value=5)
        assert q.validate_answer(0) is False
        assert q.validate_answer(6) is False

    def test_validate_non_integer(self):
        q = ScaleQuestion("Rate", min_value=1, max_value=5)
        assert q.validate_answer(3.5) is False
        assert q.validate_answer("3") is False

class TestSurvey:
    def test_create_survey(self):
        s = Survey("Customer Satisfaction", "Annual survey")
        assert s.title == "Customer Satisfaction"
        assert s.description == "Annual survey"
        assert s.status == SurveyStatus.DRAFT
        assert len(s.questions) == 0
        assert len(s.responses) == 0

    def test_add_question_to_draft(self):
        s = Survey("Test Survey")
        q = TextQuestion("Question 1")
        s.add_question(q)
        assert len(s.questions) == 1
        assert s.questions[0] == q

    def test_cannot_add_question_to_published(self):
        s = Survey("Test Survey")
        q = TextQuestion("Question 1")
        s.add_question(q)
        s.publish()
        with pytest.raises(ValueError):
            s.add_question(TextQuestion("Question 2"))

    def test_remove_question(self):
        s = Survey("Test Survey")
        q1 = TextQuestion("Question 1")
        q2 = TextQuestion("Question 2")
        s.add_question(q1)
        s.add_question(q2)
        assert s.remove_question(q1.id) is True
        assert len(s.questions) == 1
        assert s.questions[0] == q2

    def test_publish_survey(self):
        s = Survey("Test Survey")
        s.add_question(TextQuestion("Question 1"))
        s.publish()
        assert s.status == SurveyStatus.PUBLISHED

    def test_cannot_publish_empty_survey(self):
        s = Survey("Test Survey")
        with pytest.raises(ValueError):
            s.publish()

    def test_add_response(self):
        s = Survey("Test Survey")
        q1 = TextQuestion("Name")
        q2 = ScaleQuestion("Rating", 1, 5)
        s.add_question(q1)
        s.add_question(q2)
        s.publish()
        response_id = s.add_response({
            q1.id: "John Doe",
            q2.id: 5
        })
        assert response_id is not None
        assert len(s.responses) == 1

    def test_add_response_to_draft_fails(self):
        s = Survey("Test Survey")
        q = TextQuestion("Name")
        s.add_question(q)
        with pytest.raises(ValueError):
            s.add_response({q.id: "John"})

    def test_add_response_missing_answer(self):
        s = Survey("Test Survey")
        q1 = TextQuestion("Name")
        q2 = TextQuestion("Email")
        s.add_question(q1)
        s.add_question(q2)
        s.publish()
        with pytest.raises(ValueError):
            s.add_response({q1.id: "John"})

    def test_add_response_invalid_answer(self):
        s = Survey("Test Survey")
        q = ScaleQuestion("Rating", 1, 5)
        s.add_question(q)
        s.publish()
        with pytest.raises(ValueError):
            s.add_response({q.id: 10})

    def test_get_results(self):
        s = Survey("Test Survey")
        q1 = MultipleChoiceQuestion("Color", ["Red", "Blue", "Green"])
        q2 = ScaleQuestion("Rating", 1, 5)
        s.add_question(q1)
        s.add_question(q2)
        s.publish()
        s.add_response({q1.id: "Red", q2.id: 5})
        s.add_response({q1.id: "Blue", q2.id: 4})
        s.add_response({q1.id: "Red", q2.id: 5})
        results = s.get_results()
        assert results["response_count"] == 3
        assert len(results["questions"]) == 2
        mc_results = results["questions"][0]
        assert mc_results["distribution"]["Red"]["count"] == 2
        assert mc_results["distribution"]["Blue"]["count"] == 1
        scale_results = results["questions"][1]
        assert scale_results["average"] == 4.67
        assert scale_results["min"] == 4
        assert scale_results["max"] == 5
