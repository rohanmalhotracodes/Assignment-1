import os
import re
import tempfile
import smtplib
from email.message import EmailMessage

import pandas as pd
from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "topsis-web-secret")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def parse_weights_impacts(weights_s: str, impacts_s: str):
    w_parts = [x.strip() for x in weights_s.split(",")]
    i_parts = [x.strip() for x in impacts_s.split(",")]

    if not w_parts or not i_parts or any(x == "" for x in w_parts) or any(x == "" for x in i_parts):
        raise ValueError("Impacts and weights must be separated by ',' (comma).")

    try:
        weights = [float(x) for x in w_parts]
    except Exception:
        raise ValueError("Weights must be numeric values separated by commas.")

    impacts = i_parts
    if any(x not in ["+", "-"] for x in impacts):
        raise ValueError("Impacts must be either + or -.")

    return weights, impacts


def read_uploaded_file(file_storage) -> pd.DataFrame:
    name = (file_storage.filename or "").lower()
    if name.endswith(".csv"):
        return pd.read_csv(file_storage)
    if name.endswith(".xlsx") or name.endswith(".xls"):
        return pd.read_excel(file_storage)
    raise ValueError("Only .csv or .xlsx files are supported.")


def topsis(df: pd.DataFrame, weights, impacts) -> pd.DataFrame:
    if df.shape[1] < 3:
        raise ValueError("Input file must contain three or more columns.")

    criteria = df.iloc[:, 1:].copy()

    # Validate numeric criteria columns (2nd to last)
    for col in criteria.columns:
        coerced = pd.to_numeric(criteria[col], errors="coerce")
        if coerced.isna().any():
            raise ValueError("From 2nd to last columns must contain numeric values only.")
        criteria[col] = coerced

    n = criteria.shape[1]
    if len(weights) != n or len(impacts) != n:
        raise ValueError("Number of weights, impacts and criteria columns must be the same.")

    # Normalize (vector normalization)
    denom = (criteria ** 2).sum(axis=0).pow(0.5).replace(0, 1.0)
    norm = criteria / denom

    # Apply weights
    weighted = norm * pd.Series(weights, index=criteria.columns)

    # Ideal best/worst
    ideal_best = {}
    ideal_worst = {}
    for col, imp in zip(criteria.columns, impacts):
        if imp == "+":
            ideal_best[col] = weighted[col].max()
            ideal_worst[col] = weighted[col].min()
        else:
            ideal_best[col] = weighted[col].min()
            ideal_worst[col] = weighted[col].max()

    ideal_best = pd.Series(ideal_best)
    ideal_worst = pd.Series(ideal_worst)

    d_best = ((weighted - ideal_best) ** 2).sum(axis=1).pow(0.5)
    d_worst = ((weighted - ideal_worst) ** 2).sum(axis=1).pow(0.5)

    score = d_worst / (d_best + d_worst)

    out = df.copy()
    out["Topsis Score"] = score
    out["Rank"] = out["Topsis Score"].rank(ascending=False, method="dense").astype(int)
    return out


def send_email(to_email: str, attachment_path: str):
    host = os.environ.get("SMTP_HOST")
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER")
    pwd = os.environ.get("SMTP_PASS")

    if not host or not user or not pwd:
        raise RuntimeError("SMTP credentials missing. Set SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS in Replit Secrets.")

    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = to_email
    msg["Subject"] = "TOPSIS Result"
    msg.set_content("Attached is your TOPSIS output CSV (with Topsis Score and Rank).")

    with open(attachment_path, "rb") as f:
        data = f.read()

    msg.add_attachment(data, maintype="text", subtype="csv", filename="topsis_result.csv")

    with smtplib.SMTP(host, port) as s:
        s.starttls()
        s.login(user, pwd)
        s.send_message(msg)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        f = request.files.get("file")
        weights_s = (request.form.get("weights") or "").strip()
        impacts_s = (request.form.get("impacts") or "").strip()
        email = (request.form.get("email") or "").strip()

        if not f or f.filename == "":
            flash("Please upload input file.")
            return redirect("/")

        if not EMAIL_RE.match(email):
            flash("Format of email id must be correct.")
            return redirect("/")

        try:
            weights, impacts = parse_weights_impacts(weights_s, impacts_s)
            df = read_uploaded_file(f)
            res = topsis(df, weights, impacts)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
                out_path = tmp.name
            res.to_csv(out_path, index=False)

            # result emailed successfully
            send_email(email, out_path)
            flash("Result emailed successfully!")
            return redirect("/")

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            flash(str(e))
            return redirect("/")

    return render_template("index.html")


if __name__ == "__main__":
    # Replit serves via 0.0.0.0 and PORT
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
