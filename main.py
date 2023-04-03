from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap4
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, SelectField
from wtforms.validators import URL, DataRequired, InputRequired, IPAddress
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = 'TYPE WHATEVER KEY HERE, JUST BE RANDOM'
bootstrap = Bootstrap4(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location URL', validators=[URL()])
    open_time = TimeField('Open time', validators=[InputRequired(message="Enter in %H:%M format")])
    close_time = TimeField('Close_time', validators=[InputRequired(message="Enter in %H:%M format")])
    coffee = SelectField('coffee rating', choices=['☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'], validators=[DataRequired()])
    wifi = SelectField('WiFi rating', choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'], validators=[DataRequired()])
    power = SelectField('Power Outlet rating', choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'], validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    if form.validate_on_submit():
        print("True")
        print(form.location)
        with open('cafe-data.csv', "a", encoding="UTF-8", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([form.cafe.data, form.location.data, form.open_time.data, form.close_time.data, form.coffee.data, form.wifi.data, form.power.data])

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', encoding="UTF-8", newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
