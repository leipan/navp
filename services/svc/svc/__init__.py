from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('../settings.cfg')
UPLOAD_FOLDER = '/home/jpluser/m2020/imgreg_services/services/svc/svc/static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


import svc.services
import svc.views
import svc.src
