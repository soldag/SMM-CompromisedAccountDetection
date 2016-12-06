from flask import Flask
from flask import request
from flask import render_template

from core import prepare_data
from core import run_pipeline

import urllib.parse as url_parser

app = Flask(__name__)


@app.route('/check/', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        url = request.form.get('account_url', 'hpi_de')
        parsed_url = url_parser.urlparse(url)
        user_id = url_parser.parse_qs(parsed_url.query)
        status_updates = prepare_data('twitter', user_id=user_id)
        tp, tn, fp, fn = run_pipeline(status_updates, 'decision_tree')
        return 'tp: ' + str(tp) + ', tn: ' + str(tn) + ', fp: ' + str(fp) + ', tn: ' + str(tn)
    else:
        return render_template('check.html')
