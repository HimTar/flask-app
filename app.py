from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Creating a new Flask App
app = Flask(__name__)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

db = SQLAlchemy(app)

# SQL Models
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable=False)
    designation = db.Column(db.String(120), nullable=False)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    manager = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    
# Home Route
@app.route("/")
def home():
    employees = Employee.query.order_by(Employee.id).all()
    department = Department.query.order_by(Department.id).all()

    return render_template("index.html", employees = employees, department = department)

# API to add new employee
@app.route("/employee", methods = ["POST"])
def addEmployee():

        name = request.form["name"]
        designation = request.form["designation"]

        new_employee = Employee(name = name, designation = designation)

        try:
            db.session.add(new_employee)
            db.session.commit()
            return redirect("/")

        except:
            return "An unknown error occured"

# API to delete employee
@app.route("/delete-employee/<int:id>")
def deleteEmployee(id):
    to_delete = Employee.query.get_or_404(id)

    try:
        db.session.delete(to_delete)
        db.session.commit()
        return redirect("/")

    except:
        return "An unknown error occured"

# API to add new department
@app.route("/department", methods = ["POST"])
def addDepartment():
    name = request.form["dept_name"]
    manager = request.form["manager"]
    new_dept = Department(name=name,manager=manager)

    try:
        db.session.add(new_dept)
        db.session.commit()
        return redirect("/")

    except:
        return "An unknown error occured"

# API to delete Department
@app.route("/delete-department/<int:id>")
def deleteDept(id):
    to_delete = Department.query.get_or_404(id)

    try:
        db.session.delete(to_delete)
        db.session.commit()
        return redirect("/")

    except:
        return "An unknown error occured"

# 404 Handling
@app.route("/*")
def notFound():
    return "404 Not Found"

if __name__ == "__main__":
    app.run(debug=True)