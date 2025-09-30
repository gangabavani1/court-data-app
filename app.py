from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from models import db, CaseQuery
from scraper import fetch_case_details, download_judgement
import os
app = Flask(__name__)
app.secret_key = "secret123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cases.db"
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        case_type = request.form["case_type"]
        case_number = request.form["case_number"]
        year = request.form["year"]

        try:
            details = fetch_case_details(case_type, case_number, year)
            if not details:
                flash("No data found. Please check inputs.", "danger")
                return redirect(url_for("index"))

            # Save to DB
            query = CaseQuery(
                case_type=case_type,
                case_number=case_number,
                year=year,
                parties=details.get("parties"),
                filing_date=details.get("filing_date"),
                next_hearing_date=details.get("next_hearing_date"),
                status=details.get("status"),
            )
            db.session.add(query)
            db.session.commit()

            return render_template("result.html", details=details, query_id=query.id)

        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for("index"))

    return render_template("index.html")


@app.route("/download/<int:query_id>")
def download(query_id):
    query = CaseQuery.query.get_or_404(query_id)
    filepath = download_judgement(query.case_type, query.case_number, query.year)

    if filepath:
        return send_file(filepath, as_attachment=True)
    else:
        flash("Judgement not available for download.", "warning")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)


