from flask import Blueprint
import apicefet.schedule as schedule

schedule_bp = Blueprint('token', __name__)
schedule_bp.add_url_rule('', 'time', schedule.schedules)
