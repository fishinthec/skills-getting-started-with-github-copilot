"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}

# Additional activities: 2 sports, 2 artistic, 2 intellectual
activities.update({
    "Soccer Club": {
        "description": "Outdoor soccer practice and friendly matches",
        "schedule": "Wednesdays and Saturdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu"]
    },
    "Swimming Team": {
        "description": "Lap training, technique work, and meets",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 6:30 PM",
        "max_participants": 18,
        "participants": ["mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Drawing, painting and weekly critiques",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["sophia@mergington.edu"]
    },
    "Theater Workshop": {
        "description": "Acting exercises, scene study, and small productions",
        "schedule": "Mondays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["noah@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Problem solving club preparing for math competitions",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["emma@mergington.edu"]
    },
    "Science Bowl": {
        "description": "Team-based science trivia and quick-response practice",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 12,
        "participants": ["alex@mergington.edu"]
    }
})


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Normalize email to avoid case/whitespace duplicates
    normalized = email.strip().lower()

    # Reject duplicate signups
    existing = [p.strip().lower() for p in activity.get("participants", [])]
    if normalized in existing:
        raise HTTPException(status_code=400, detail="Student is already signed up")

    # Enforce capacity
    if len(activity.get("participants", [])) >= activity.get("max_participants", 0):
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def unregister_participant(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    normalized = email.strip().lower()
    participants = activity.get("participants", [])
    # Find matching participant by normalized email
    for i, p in enumerate(participants):
        if p.strip().lower() == normalized:
            participants.pop(i)
            return {"message": f"Unregistered {email} from {activity_name}"}

    raise HTTPException(status_code=404, detail="Participant not found")
