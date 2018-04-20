from database import db_session
from models.models import MeetingReport


def get_all_report_for_user(user):
    return MeetingReport.query.filter_by(user=user).all()