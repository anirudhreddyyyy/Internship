from database import db
from datetime import datetime

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    content = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
