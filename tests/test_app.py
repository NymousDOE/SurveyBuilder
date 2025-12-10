"""
Integration tests for Flask API
"""

import pytest
import json
import tempfile
import os

from src.app import app
from src.storage import SurveyStorage, get_storage


@pytest.fixture
def client():
    """Create test client"""
    # Setup temporary storage
    temp_file = tempfile.NamedTemporaryFile(
        mode='w',
        delete=False,
        suffix='.json'
    )
    temp_file.close()
    
    # Configure app for testing
    app.config['TESTING'] = True
    
    # Replace global storage with test storage
    import src.app
    src.app.storage = SurveyStorage(storage_path=temp_file.name)
    
    with app.test_client() as client:
        yield client
    
    # Cleanup
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)


class TestHealthCheck:
    """Tests for health check endpoint"""
    
    def test_health_check(self, client):
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'


class TestSurveyEndpoints:
    """Tests for survey endpoints"""
    
    def test_create_survey(self, client):
        response = client.post(
            '/surveys',
            data=json.dumps({
                'title': 'Test Survey',
                'description': 'Test description'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == 'Test Survey'
        assert data['description'] == 'Test description'
        assert 'id' in data
    
    def test_create_survey_without_title(self, client):
        response = client.post(
            '/surveys',
            data=json.dumps({'description': 'No title'}),
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_list_surveys(self, client):
        # Create some surveys
        client.post(
            '/surveys',
            data=json.dumps({'title': 'Survey 1'}),
            content_type='application/json'
        )
        client.post(
            '/surveys',
            data=json.dumps({'title': 'Survey 2'}),
            content_type='application/json'
        )
        
        response = client.get('/surveys')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 2
        assert len(data['surveys']) == 2
    
    def test_get_survey(self, client):
        # Create survey
        create_response = client.post(
            '/surveys',
            data=json.dumps({'title': 'Test Survey'}),
            content_type='application/json'
        )
        survey_id = json.loads(create_response.data)['id']
        
        # Get survey
        response = client.get(f'/surveys/{survey_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == survey_id
    
    def test_get_nonexistent_survey(self, client):
        response = client.get('/surveys/nonexistent')
        assert response.status_code == 404
    
    def test_delete_survey(self, client):
        # Create survey
        create_response = client.post(
            '/surveys',
            data=json.dumps({'title': 'Test Survey'}),
            content_type='application/json'
        )
        survey_id = json.loads(create_response.data)['id']
        
        # Delete survey
        response = client.delete(f'/surveys/{survey_id}')
        assert response.status_code == 200
        
        # Verify deleted
        get_response = client.get(f'/surveys/{survey_id}')
        assert get_response.status_code == 404


class TestQuestionEndpoints:
    """Tests for question endpoints"""
    
    def test_add_text_question(self, client):
        # Create survey
        survey_response = client.post(
            '/surveys',
            data=json.dumps({'title': 'Test Survey'}),
            content_type='application/json'
        )
        survey_id = json.loads(survey_response.data)['id']
        
        # Add question
        response = client.post(
            f'/surveys/{survey_id}/questions',
            data=json.dumps({
                'type': 'text',
                'text': 'What is your name?'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['type'] == 'text'
        assert data['text'] == 'What is your name?'
    
    def test_add_multiple_choice_question(self, client):
        survey_response = client.post(
            '/surveys',
            data=json.dumps({'title': 'Test Survey'}),
            content_type='application/json'
        )
        survey_id = json.loads(survey_response.data)['id']
        
        response = client.post(
            f'/surveys/{survey_id}/questions',
            data=json.dumps({
                'type': 'multiple_choice',
                'text': 'Choose color',
                'options': ['Red', 'Blue', 'Green']
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert len(data['options']) == 3
    
    def test_get_questions(self, client):
        survey_response = client.post(
            '/surveys',
            data=json.dumps({'title': 'Test Survey'}),
            content_type='application/json'
        )
        survey_id = json.loads(survey_response.data)['id']
        
        # Add questions
        client.post(
            f'/surveys/{survey_id}/questions',
            data=json.dumps({'type': 'text', 'text': 'Q1'}),
            content_type='application/json'
        )
        client.post(
            f'/surveys/{survey_id}/questions',
            data=json.dumps({'type': 'text', 'text': 'Q2'}),
            content_type='application/json'
        )
        
        response = client.get(f'/surveys/{survey_id}/questions')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 2


class TestSurveyWorkflow:
    """End-to-end workflow tests"""
    
    def test_complete_survey_workflow(self, client):
        # 1. Create survey
        survey_response = client.post(
            '/surveys',
            data=json.dumps({
                'title': 'Customer Satisfaction',
                'description': 'Annual survey'
            }),
            content_type='application/json'
        )
        assert survey_response.status_code == 201
        survey_id = json.loads(survey_response.data)['id']
        
        # 2. Add questions
        q1_response = client.post(
            f'/surveys/{survey_id}/questions',
            data=json.dumps({
                'type': 'text',
                'text': 'What is your name?'
            }),
            content_type='application/json'
        )
        q1_id = json.loads(q1_response.data)['id']
        
        q2_response = client.post(
            f'/surveys/{survey_id}/questions',
            data=json.dumps({
                'type': 'scale',
                'text': 'Rate our service',
                'min_value': 1,
                'max_value': 5
            }),
            content_type='application/json'
        )
        q2_id = json.loads(q2_response.data)['id']
        
        # 3. Publish survey
        publish_response = client.post(
            f'/surveys/{survey_id}/publish'
        )
        assert publish_response.status_code == 200
        
        # 4. Submit response
        response_data = {
            'responses': [
                {'question_id': q1_id, 'answer': 'John Doe'},
                {'question_id': q2_id, 'answer': 5}
            ]
        }
        submit_response = client.post(
            f'/surveys/{survey_id}/responses',
            data=json.dumps(response_data),
            content_type='application/json'
        )
        assert submit_response.status_code == 201
        
        # 5. Get results
        results_response = client.get(f'/surveys/{survey_id}/results')
        assert results_response.status_code == 200
        results = json.loads(results_response.data)
        assert results['response_count'] == 1
