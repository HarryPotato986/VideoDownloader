from key import SECRET_KEY
from flask import Flask, render_template, url_for, request, send_file, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import uuid
from VideoDownloader import Download
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)


def get_guest_uuid():
    if 'guest_uuid' not in session:
        session['guest_uuid'] = str(uuid.uuid4())
    return session['guest_uuid']

class Save(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    file_name = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    guest_id = get_guest_uuid()

    if request.method == 'POST':
        if "download" in request.form:
            entry = db.session.get(Save, guest_id)
            if entry is None:
                return render_template('index.html', is_done=True, failed=True, message="Something went very worng, you should never see this message!")
            
            return send_file(entry.file_path, download_name=entry.file_name, as_attachment=True)
        
        else:
            text = request.form['link']
            res = request.form['resolution']
            bitrate = request.form['audioq']

            result = Download(text, res, bitrate, "working-files/" + str(guest_id))

            if os.path.isfile(result[0]):
                new_entry = Save(id=guest_id, file_path=result[0], file_name=result[1])
                db.session.add(new_entry)
                db.session.commit()

                return render_template('index.html', is_done=True, failed=False, message=f"{result[1]} is ready to download")
            else:
                return render_template('index.html', is_done=True, failed=True, message=result[0])
        
    else:
        return render_template('index.html', is_done=False)
    
@app.route('/test')
def test():
    return send_file("working-files/video.mp4", download_name="test.mp4", as_attachment=True)

@app.route('/uuidtest')
def uuidtest():
    guest_id = get_guest_uuid()
    return f"Hello, Guest! Your UUID is: {guest_id}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)