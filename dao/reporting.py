import datetime

from models.models import MeetingReport


def get_all_report_for_user(user):
    return MeetingReport.query.filter_by(user=user).all()


def get_today_reporting(user):
    return MeetingReport.query.filter_by(user=user).filter_by(date_report=datetime.date.today()).all()


def get_today_reporting_for_team(team_id):
    return MeetingReport.query.filter_by(team=team_id).all()
