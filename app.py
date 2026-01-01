from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# ------------------ HTML TEMPLATE ------------------ #
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Health & BMI Calculator (Flask + Docker)</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: #e5e7eb;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
            margin: 0;
            padding: 40px 0;
        }
        .container {
            background: #020617;
            border-radius: 12px;
            padding: 24px 32px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.6);
            width: 480px;
        }
        h1, h2 {
            margin-top: 0;
            color: #38bdf8;
        }
        label {
            display: block;
            margin-top: 12px;
            font-size: 14px;
        }
        input, select {
            width: 100%;
            padding: 8px 10px;
            margin-top: 4px;
            border-radius: 6px;
            border: 1px solid #4b5563;
            background: #020617;
            color: #e5e7eb;
        }
        button {
            margin-top: 18px;
            width: 100%;
            padding: 10px;
            border-radius: 6px;
            border: none;
            background: #22c55e;
            color: #022c22;
            font-weight: bold;
            cursor: pointer;
        }
        button:hover {
            background: #16a34a;
        }
        .result {
            margin-top: 20px;
            padding: 12px;
            border-radius: 8px;
            background: #0f172a;
        }
        .badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 999px;
            font-size: 12px;
            margin-left: 6px;
        }
        .low { background: #22c55e33; color: #bbf7d0; }
        .medium { background: #facc1533; color: #facc15; }
        .high { background: #ef444433; color: #fecaca; }
        small {
            color: #9ca3af;
        }
        a {
            color: #38bdf8;
        }
        .api-info {
            margin-top: 18px;
            font-size: 13px;
            color: #9ca3af;
        }
        code {
            background: #020617;
            padding: 2px 4px;
            border-radius: 4px;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Health & BMI Calculator</h1>
    <p>Simple demo app to test <strong>Flask + Docker</strong>. Enter your details and see the BMI & risk category.</p>

    <form method="post" action="/">
        <label>Age
            <input type="number" name="age" min="1" max="120" value="{{ age or '' }}" required>
        </label>

        <label>Height (meters)
            <input type="number" step="0.01" name="height" min="0.5" max="2.5" value="{{ height or '' }}" required>
        </label>

        <label>Weight (kg)
            <input type="number" step="0.1" name="weight" min="10" max="300" value="{{ weight or '' }}" required>
        </label>

        <label>Smoker?
            <select name="smoker">
                <option value="no" {% if smoker == 'no' %}selected{% endif %}>No</option>
                <option value="yes" {% if smoker == 'yes' %}selected{% endif %}>Yes</option>
            </select>
        </label>

        <button type="submit">Calculate</button>
    </form>

    {% if result %}
    <div class="result">
        <h2>Result</h2>
        <p>BMI: <strong>{{ result.bmi }}</strong></p>
        <p>
            Category:
            <strong>{{ result.bmi_category }}</strong>
            <span class="badge {{ result.risk_level }}">{{ result.risk_level|capitalize }} risk</span>
        </p>
        <p>Message: {{ result.message }}</p>
    </div>
    {% endif %}

    <div class="api-info">
        <p><strong>API endpoints in this container:</strong></p>
        <ul>
            <li><code>GET /api/health</code> → status info</li>
            <li><code>POST /api/bmi</code> → JSON BMI calculator</li>
        </ul>
        <p>
            Example JSON for <code>/api/bmi</code>:
        </p>
        <pre>{
  "age": 30,
  "height": 1.75,
  "weight": 70,
  "smoker": false
}</pre>
    </div>
</div>
</body>
</html>
"""

# ------------------ CORE LOGIC ------------------ #
def compute_bmi(weight: float, height: float) -> float:
    """Return BMI rounded to 2 decimals."""
    return round(weight / (height ** 2), 2)


def categorize_bmi(bmi: float) -> str:
    if bmi < 18.5:
        return "underweight"
    elif bmi < 25:
        return "normal"
    elif bmi < 30:
        return "overweight"
    else:
        return "obese"


def risk_from_bmi_and_smoker(bmi: float, smoker: bool) -> str:
    if bmi >= 30 or (smoker and bmi >= 25):
        return "high"
    elif bmi >= 25 or smoker:
        return "medium"
    else:
        return "low"


def risk_message(risk: str) -> str:
    if risk == "low":
        return "Your risk level is low. Keep maintaining a healthy lifestyle."
    if risk == "medium":
        return "Your risk level is moderate. Consider regular exercise and a balanced diet."
    return "Your risk level is high. It may be worth talking to a doctor or nutritionist."


# ------------------ WEB ROUTES ------------------ #
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    form_data = {"age": None, "height": None, "weight": None, "smoker": "no"}

    if request.method == "POST":
        try:
            age = int(request.form.get("age"))
            height = float(request.form.get("height"))
            weight = float(request.form.get("weight"))
            smoker_str = request.form.get("smoker", "no")

            form_data.update(
                age=age,
                height=height,
                weight=weight,
                smoker=smoker_str,
            )

            smoker = smoker_str == "yes"
            bmi = compute_bmi(weight, height)
            bmi_cat = categorize_bmi(bmi)
            risk_level = risk_from_bmi_and_smoker(bmi, smoker)

            result = {
                "bmi": bmi,
                "bmi_category": bmi_cat,
                "risk_level": risk_level,
                "message": risk_message(risk_level),
            }
        except (TypeError, ValueError):
            result = {
                "bmi": None,
                "bmi_category": "invalid",
                "risk_level": "high",
                "message": "Invalid input. Please enter numeric values.",
            }

    return render_template_string(HTML_TEMPLATE, result=result, **form_data)


# ------------------ JSON API ROUTES ------------------ #
@app.route("/api/health", methods=["GET"])
def api_health():
    """Simple health check endpoint."""
    return jsonify(
        {
            "status": "ok",
            "service": "Flask BMI Demo",
            "message": "Container is running",
        }
    )


@app.route("/api/bmi", methods=["POST"])
def api_bmi():
    """
    Expects JSON:
    {
      "age": 30,
      "height": 1.75,
      "weight": 70,
      "smoker": false
    }
    """
    data = request.get_json(force=True, silent=True) or {}
    missing = [k for k in ("age", "height", "weight", "smoker") if k not in data]

    if missing:
        return (
            jsonify(
                {
                    "error": "Missing required fields",
                    "missing": missing,
                }
            ),
            400,
        )

    try:
        age = int(data["age"])
        height = float(data["height"])
        weight = float(data["weight"])
        smoker = bool(data["smoker"])
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid field types"}), 400

    bmi = compute_bmi(weight, height)
    bmi_cat = categorize_bmi(bmi)
    risk_level = risk_from_bmi_and_smoker(bmi, smoker)

    return jsonify(
        {
            "age": age,
            "height": height,
            "weight": weight,
            "smoker": smoker,
            "bmi": bmi,
            "bmi_category": bmi_cat,
            "risk_level": risk_level,
            "message": risk_message(risk_level),
        }
    )


# ------------------ ENTRYPOINT ------------------ #
if __name__ == "__main__":
    # host=0.0.0.0 is important for Docker
    app.run(host="0.0.0.0", port=5000, debug=True)

