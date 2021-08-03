from app import db
from flask import Blueprint
from flask import request
from flask import jsonify, make_response
from .models.event import Event


events_bp = Blueprint("events", __name__, url_prefix="/events")


def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False

# gets single event, new route


@events_bp.route("/<event_id>", methods=["GET", "PUT", "DELETE"])
def get_single_event(event_id):
    event = Event.query.get(event_id)

    if not is_int(event_id):
        return {
            "message": f"ID {event_id} must be a number",
            "success": False
        }, 400

    if request.method == "GET":
        if event is None:
            return make_response("none", 404)
        return {
            "id": event.event_id,
            "title": event.title,
            "location": event.location,
            "description": event.description,
            "date": event.date
        }, 200

    elif request.method == "DELETE":
        db.session.delete(event)
        db.session.commit()
        return (f"Event #{event.event_id} successfully deleted")


@events_bp.route("", methods=["GET"], strict_slashes=False)
def all_events():

    # if request.method == "GET":
    #     title_query = request.args.get("date", 'asc')
    #     if title_query:
    #         events = Event.query.filter_by(title=title_query)
    #     else:
    #         events = Event.query.all()
    events = Event.query.all()
    events_response = []

    for event in events:
        events_response.append({
            "id": event.event_id,
            "title": event.title,
            "location": event.location,
            "description": event.description,
            "date": event.date
        })
    return jsonify(events_response), 200


@events_bp.route("", methods=["POST"])
def handle_events():
    request_body = request.get_json()
    event = Event(title=request_body["title"],
                  description=request_body["description"],
                  location=request_body["location"],
                  date=request_body["date"])

    db.session.add(event)
    db.session.commit()

    return make_response({"event": event.return_task_json()}, 201)
