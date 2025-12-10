import pytest
import os
import tempfile

from src.storage import SurveyStorage
from src.models import QuestionType


class TestSurveyStorage:
    @pytest.fixture
    def temp_storage(self):
        temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json")
        temp_file.close()
        storage = SurveyStorage(storage_path=temp_file.name)
        yield storage
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

    def test_create_survey(self, temp_storage):
        survey = temp_storage.create_survey("Test Survey", "Description")
        assert survey.title == "Test Survey"
        assert survey.description == "Description"
        assert survey.id in temp_storage.surveys

    def test_get_survey(self, temp_storage):
        survey = temp_storage.create_survey("Test")
        retrieved = temp_storage.get_survey(survey.id)
        assert retrieved is not None
        assert retrieved.id == survey.id

    def test_get_nonexistent_survey(self, temp_storage):
        assert temp_storage.get_survey("nonexistent") is None

    def test_list_surveys(self, temp_storage):
        temp_storage.create_survey("Survey 1")
        temp_storage.create_survey("Survey 2")
        temp_storage.create_survey("Survey 3")
        surveys = temp_storage.list_surveys()
        assert len(surveys) == 3

    def test_delete_survey(self, temp_storage):
        survey = temp_storage.create_survey("Test")
        assert temp_storage.delete_survey(survey.id) is True
        assert temp_storage.get_survey(survey.id) is None

    def test_delete_nonexistent_survey(self, temp_storage):
        assert temp_storage.delete_survey("nonexistent") is False

    def test_add_text_question(self, temp_storage):
        survey = temp_storage.create_survey("Test")
        question = temp_storage.add_question_to_survey(
            survey.id, "text", "What is your name?"
        )
        assert question.type == QuestionType.TEXT
        assert question.text == "What is your name?"
        assert len(survey.questions) == 1

    def test_add_multiple_choice_question(self, temp_storage):
        survey = temp_storage.create_survey("Test")
        question = temp_storage.add_question_to_survey(
            survey.id,
            "multiple_choice",
            "Choose color",
            options=["Red", "Blue", "Green"],
        )
        assert question.type == QuestionType.MULTIPLE_CHOICE
        assert len(question.options) == 3

    def test_add_scale_question(self, temp_storage):
        survey = temp_storage.create_survey("Test")
        question = temp_storage.add_question_to_survey(
            survey.id, "scale", "Rate us", min_value=1, max_value=10
        )
        assert question.type == QuestionType.SCALE
        assert question.min_value == 1
        assert question.max_value == 10

    def test_persistence(self, temp_storage):
        survey = temp_storage.create_survey("Test Survey")
        temp_storage.add_question_to_survey(survey.id, "text", "Question 1")
        temp_storage.add_question_to_survey(
            survey.id, "multiple_choice", "Question 2", options=["A", "B", "C"]
        )
        new_storage = SurveyStorage(storage_path=temp_storage.storage_path)
        assert len(new_storage.surveys) == 1
        loaded_survey = new_storage.get_survey(survey.id)
        assert loaded_survey is not None
        assert loaded_survey.title == "Test Survey"
        assert len(loaded_survey.questions) == 2
