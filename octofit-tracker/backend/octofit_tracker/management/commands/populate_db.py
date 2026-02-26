from django.core.management.base import BaseCommand
from django.db import connection
from djongo import models

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Drop collections if they exist
        db = connection.cursor().db_conn.client['octofit_db']
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create test users
        users = [
            {"name": "Superman", "email": "superman@dc.com", "team": "dc"},
            {"name": "Batman", "email": "batman@dc.com", "team": "dc"},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "dc"},
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "marvel"},
            {"name": "Captain America", "email": "cap@marvel.com", "team": "marvel"},
            {"name": "Black Widow", "email": "widow@marvel.com", "team": "marvel"},
        ]
        db.users.insert_many(users)
        db.users.create_index([("email", 1)], unique=True)

        # Create teams
        teams = [
            {"name": "marvel", "members": ["Iron Man", "Captain America", "Black Widow"]},
            {"name": "dc", "members": ["Superman", "Batman", "Wonder Woman"]},
        ]
        db.teams.insert_many(teams)

        # Create activities
        activities = [
            {"user": "Superman", "activity": "Flying", "duration": 120},
            {"user": "Iron Man", "activity": "Running", "duration": 60},
            {"user": "Batman", "activity": "Martial Arts", "duration": 90},
        ]
        db.activities.insert_many(activities)

        # Create leaderboard
        leaderboard = [
            {"team": "marvel", "points": 300},
            {"team": "dc", "points": 250},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Create workouts
        workouts = [
            {"user": "Superman", "workout": "Strength", "suggestion": "Lift heavy objects"},
            {"user": "Iron Man", "workout": "Cardio", "suggestion": "Run 5km"},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data'))
