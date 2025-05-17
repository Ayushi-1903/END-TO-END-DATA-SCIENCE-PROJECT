from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Load saved model
with open('student_pass_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html', result=None)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        studytime = float(request.form['studytime'])
        failures = int(request.form['failures'])
        absences = int(request.form['absences'])
        sex = request.form['sex']

        # Prepare input DataFrame
        input_df = pd.DataFrame([[studytime, failures, absences, sex]],
                                columns=['studytime', 'failures', 'absences', 'sex'])
        input_df = pd.get_dummies(input_df, drop_first=True)

        # Ensure all columns present
        for col in model.feature_names_in_:
            if col not in input_df.columns:
                input_df[col] = 0

        prediction = model.predict(input_df)[0]
        result = "Pass" if prediction == 1 else "Fail"
    except Exception as e:
        result = f"Error: {str(e)}"

    return render_template('Index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
