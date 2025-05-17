from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__, template_folder='Template')

# -------------------------
# Basic Pass/Fail Prediction Logic
# -------------------------
def predict_pass(python, c_programming, dsa, dmp):
    """
    Predicts if a student passes or fails based on their scores.

    Args:
        python (float): Python score.
        c_programming (float): C Programming score.
        dsa (float): DSA score.
        dmp (float): DMP score.

    Returns:
        tuple: A tuple containing the result ('Pass' or 'Fail') and the average score.
    """
    scores = [python, c_programming, dsa, dmp]
    avg_score = sum(scores) / len(scores)
    if avg_score >= 50:
        return 'Pass', avg_score
    else:
        return 'Fail', avg_score

# -------------------------
# Routes
# -------------------------
@app.route('/')
def home():
    """
    Renders the home page (Index.html).
    """
    return render_template('Index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Handles the prediction of student results based on submitted form data.
    """
    try:
        student_name = request.form['student_name']
        python_score = float(request.form['python'])
        c_program_score = float(request.form['c_program'])
        dsa_score = float(request.form['dsa'])
        dmp_score = float(request.form['dmp'])

        result, avg_score = predict_pass(python_score, c_program_score, dsa_score, dmp_score)
        total = python_score + c_program_score + dsa_score + dmp_score
        return render_template(
            'Index.html',
            student_name=student_name,
            result=result,
            python=python_score,
            c_program=c_program_score,
            dsa=dsa_score,
            dmp=dmp_score,
            total=total,
            probability=round((avg_score / 100) * 100, 2)
        )
    except ValueError:
        return render_template('Index.html', error="Invalid input. Please enter numeric values for scores.")
    except Exception as e:
        return f"Error during prediction: {e}"

# -------------------------
# Feedback Form Routes
# -------------------------
@app.route('/feedback')
def feedback():
    """
    Renders the feedback form (feedback.html).
    """
    return render_template('feedback.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    """
    Handles the submission of feedback data, saving it to a CSV file.
    """
    try:
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Ensure the directory exists
        feedback_dir = 'feedback_data'  # Changed for clarity
        if not os.path.exists(feedback_dir):
            os.makedirs(feedback_dir)

        feedback_file_path = os.path.join(feedback_dir, 'feedback.csv') # More robust

        file_exists = os.path.isfile(feedback_file_path)
        with open(feedback_file_path, 'a', newline='', encoding='utf-8') as f: # added encoding
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Name', 'Email', 'Message'])
            writer.writerow([name, email, message])

        # Use url_for for redirection
        return redirect(url_for('thank_you', name=name))
    except Exception as e:
        return f"Error submitting feedback: {e}"

@app.route('/thank_you')
def thank_you():
    """
    Renders a thank you page after feedback submission.
    """
    name = request.args.get('name', 'User')  # Default to 'User' if no name is provided.
    return render_template('thank_you.html', name=name)

# -------------------------
# Admin Panel
# -------------------------
@app.route('/admin')
def admin():
    """
    Renders the admin panel (admin_panel.html) and displays feedback data from the CSV file.
    """
    try:
        feedback_dir = 'feedback_data' # Consistent
        feedback_file_path = os.path.join(feedback_dir, 'feedback.csv')
        feedback_data = []
        if os.path.exists(feedback_file_path):
            with open(feedback_file_path, 'r', encoding='utf-8') as f: # added encoding
                reader = csv.reader(f)
                feedback_data = list(reader)
        return render_template('admin_panel.html', feedback=feedback_data)
    except Exception as e:
        return f"Error loading admin panel: {e}"
    

if __name__ == '__main__':
    app.run(debug=True)
