from flask import Flask, request, jsonify, send_file
import csv
import io
from typing import Dict, Any

from src.storage import get_storage
from src.models import SurveyStatus

app = Flask(__name__)
storage = get_storage()


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200


@app.route("/surveys", methods=["POST"])
def create_survey():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    try:
        survey = storage.create_survey(
            title=data["title"], description=data.get("description", "")
        )
        return jsonify(survey.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/surveys", methods=["GET"])
def list_surveys():
    surveys = storage.list_surveys()
    return (
        jsonify({"surveys": [s.to_dict() for s in surveys], "count": len(surveys)}),
        200,
    )


@app.route("/surveys/<survey_id>", methods=["GET"])
def get_survey(survey_id: str):
    survey = storage.get_survey(survey_id)
    if not survey:
        return jsonify({"error": "Survey not found"}), 404
    return jsonify(survey.to_dict()), 200


@app.route("/surveys/<survey_id>", methods=["DELETE"])
def delete_survey(survey_id: str):
    if storage.delete_survey(survey_id):
        return jsonify({"message": "Survey deleted"}), 200
    return jsonify({"error": "Survey not found"}), 404


@app.route("/surveys/<survey_id>/questions", methods=["POST"])
def add_question(survey_id: str):
    data = request.get_json()
    if not data or "type" not in data or "text" not in data:
        return jsonify({"error": "Question type and text are required"}), 400
    try:
        kwargs = {}
        if data["type"] == "multiple_choice":
            if "options" not in data or len(data["options"]) < 2:
                return (
                    jsonify({"error": "Multiple choice needs at least 2 options"}),
                    400,
                )
            kwargs["options"] = data["options"]
        elif data["type"] == "scale":
            kwargs["min_value"] = data.get("min_value", 1)
            kwargs["max_value"] = data.get("max_value", 5)
        question = storage.add_question_to_survey(
            survey_id=survey_id, question_type=data["type"], text=data["text"], **kwargs
        )
        return jsonify(question.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/surveys/<survey_id>/questions", methods=["GET"])
def get_questions(survey_id: str):
    survey = storage.get_survey(survey_id)
    if not survey:
        return jsonify({"error": "Survey not found"}), 404
    return (
        jsonify(
            {
                "questions": [q.to_dict() for q in survey.questions],
                "count": len(survey.questions),
            }
        ),
        200,
    )


@app.route("/surveys/<survey_id>/publish", methods=["POST"])
def publish_survey(survey_id: str):
    survey = storage.get_survey(survey_id)
    if not survey:
        return jsonify({"error": "Survey not found"}), 404
    try:
        survey.publish()
        storage.save_to_file()
        return (
            jsonify(
                {
                    "message": "Survey published",
                    "survey_url": f"/surveys/{survey_id}/respond",
                }
            ),
            200,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/surveys/<survey_id>/responses", methods=["POST"])
def submit_response(survey_id: str):
    survey = storage.get_survey(survey_id)
    if not survey:
        return jsonify({"error": "Survey not found"}), 404
    data = request.get_json()
    if not data or "responses" not in data:
        return jsonify({"error": "Responses are required"}), 400
    try:
        responses_dict = {}
        for resp in data["responses"]:
            responses_dict[resp["question_id"]] = resp["answer"]
        response_id = survey.add_response(responses_dict)
        storage.save_to_file()
        return (
            jsonify({"message": "Response submitted", "response_id": response_id}),
            201,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/surveys/<survey_id>/results", methods=["GET"])
def get_results(survey_id: str):
    survey = storage.get_survey(survey_id)
    if not survey:
        return jsonify({"error": "Survey not found"}), 404
    return jsonify(survey.get_results()), 200


@app.route("/surveys/<survey_id>/export", methods=["GET"])
def export_results(survey_id: str):
    survey = storage.get_survey(survey_id)
    if not survey:
        return jsonify({"error": "Survey not found"}), 404
    if len(survey.responses) == 0:
        return jsonify({"error": "No responses to export"}), 400
    output = io.StringIO()
    writer = csv.writer(output)
    header = ["response_id", "timestamp"]
    header.extend([q.text for q in survey.questions])
    writer.writerow(header)
    for response in survey.responses:
        row = [response["id"], response["timestamp"]]
        for question in survey.questions:
            answer = response["answers"].get(question.id, "")
            row.append(answer)
        writer.writerow(row)
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"survey_{survey_id}_results.csv",
    )


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
