from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CaseQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_type = db.Column(db.String(50))
    case_number = db.Column(db.String(50))
    year = db.Column(db.String(10))
    parties = db.Column(db.String(200))
    filing_date = db.Column(db.String(50))
    next_hearing_date = db.Column(db.String(50))
    status = db.Column(db.String(100))