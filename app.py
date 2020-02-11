
from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, fields

from linear_model import import_model_predict

from werkzeug.middleware.proxy_fix import ProxyFix


################ Flask RestPlus ################

flask_app = Flask(__name__)
flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app)
api = Api(app = flask_app,
          version = "1.0",
		  title = "Simple Compensation Predictor",
		  description = "Simple prediction example for compensation dataset")
ns = api.namespace('simple', description='Simple Prediction API')

ns_model = api.model('predict',
		             {'yearsofexperience': fields.Float(required = True,
					                        description="value",
					                        help="Value cannot be blank",
                                            example=18.2)})

################################################

# Load the model and predict
def prediction_helper(model_path, data):
    import numpy as np
    # in reality, the dataset for prediction must go thro the same feature engineering pipeline as training dataset
    value = [[np.array(data)]]
    prediction = import_model_predict(model_path, value)
    return prediction[0]

################## Flask RestPlus APIs #########

@ns.route('/')
class HealthCheck(Resource):
    def get(self):
        return {"healthcheck": "success"}, 200

@ns.route('/predict',methods=['POST'])
class SimplePredictor(Resource):

    @ns.expect(ns_model)
    def post(self):
        # get the data from the POST request
        data = request.json['yearsofexperience']
        print("data value received is - ", data)

        # make prediction
        output = prediction_helper(model_path="model.pkl", data=data)

        print("output of prediction is ", output)
        # return output, 201
        return jsonify({'prediction_output': output,
                        'version': 1.0})


if __name__ == '__main__':
    flask_app.run(debug=True, port=5000)