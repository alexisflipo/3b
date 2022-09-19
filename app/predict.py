# from flask import Blueprint, render_template, redirect, url_for, request, flash
# from werkzeug.security import generate_password_hash, check_password_hash
# from run import db, User
# from flask_login import login_user, logout_user, login_required
# from functools import lru_cache

# predict = Blueprint("predict", __name__)


# from run import db, Books

# @lru_cache(maxsize=1024)
# @predict.route("/predict", methods=['POST'])
# def predict():

#     int_features = [int(x) for x in request.form.values()]
#     final_features = [np.array(int_features)]
#     prediction = model.predict(final_features)

#     output = round(prediction[0], 2)

#     return render_template('index.html', prediction_text='Sales should be $ {}'.format(output))

# @app.route('/results',methods=['POST'])
# def results():

#     data = request.get_json(force=True)
#     prediction = model.predict([np.array(list(data.values()))])

#     output = prediction[0]
#     return jsonify(output)
    