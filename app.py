from flask import Flask, render_template, url_for, flash, request, redirect, session
import csv
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

app.config.update(dict(SECRET_KEY='d1e6b983ae53474d2df0d3d381ef05a3'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(app)

DATA = [
	{
		'question': 'What is the name of an actor who plays Geralt of Rivia in Netflix series The Witcher?',
		'pos_answers': ['Henry Cavill', 'David Beckham', 'Bradley Cooper'],
		'correct_answer': 'Henry Cavill'
	},
	{
		'question': 'The symbol of Helium is:',
		'pos_answers': ['O', 'He', 'H'],
		'correct_answer': 'He'
	},
	{
		'question': 'What is an integer?',
		'pos_answers': ['Whole number', 'Word', 'Sentence'],
		'correct_answer': 'Whole number'
	},
	{
		'question': 'What is the name of operating system made by Microsoft?',
		'pos_answers': ['Linux', 'Mac Os', 'Windows'],
		'correct_answer': 'Windows'
	},
{
		'question': 'Which actress played with Bradley Cooper in A star is born movie?',
		'pos_answers': ['Katy Perry', 'Lady Gaga', 'Rihanna'],
		'correct_answer': 'Lady Gaga'
	},
	{
		'question': 'The result of 34+54 is: ',
		'pos_answers': ['88', '89', '78'],
		'correct_answer': '88'
	},
	{
		'question': 'How does an eukaryotic cell produce energy?',
		'pos_answers': ['By using Mitochondria ', 'It does not produce an energy', 'By using Golgi Apparatus'],
		'correct_answer': 'By using Mitochondria'
	},
	{
		'question': 'What is the name of basketball club from LA?',
		'pos_answers': ['Bulls', 'Celtics', 'Lakers'],
		'correct_answer': 'Lakers'
	},
]


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
	if request.method == 'POST':
		points = 0
		answers = request.form

		for pnr, ans in answers.items():
			if ans == DATA[int(pnr)]['correct_answer']:
				points += 1
		flash("Your result: {0}, congrats 😁".format(points))
		return redirect(url_for('quiz'))
	return render_template('quiz.html', questions=DATA)


@app.route('/user', methods=['GET', 'POST'])
def user():
	error = None
	username = ''
	if request.method == 'POST':
		if request.form['name'] == username:
			error = 'Invalid Credentials. Please try again.'
		else:
			return redirect(url_for('weather_page'))
	return render_template('user.html', error=error)


class City(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)


@app.route('/weather', methods=['GET', 'POST'])
def weather_page():
	if request.method == 'POST':
		new_city = request.form.get('city')

		if new_city:
			new_city_obj = City(name=new_city)

			db.session.add(new_city_obj)
			db.session.commit()

	cities = City.query.all()

	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=1ef4dfefeaddb3c1cc6920747b421d17'
	weather_data = []

	for city in cities:
		r = requests.get(url.format(city.name)).json()

		weather = {
			'city': city.name,
			'temperature': r['main']['temp'],
			'description': r['weather'][0]['description'],
			'icon': r['weather'][0]['icon'],
		}

		weather_data.append(weather)

	return render_template('weather2.html', weather_data=weather_data)


def write_to_file(data):
	with open('database.csv', mode='a') as database:
		name = data['field1']
		email = data['field2']
		message = data['field3']
		file = database.write(f'\n{name}, {email}, {message}')


def write_to_csv(data):
	with open('database.csv', mode='a', newline='', encoding='utf=8') as database2:
		name = data['field1']
		email = data['field2']
		message = data['field3']
		csv_writer = csv.writer(database2, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow([name, email, message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
	if request.method == 'POST':
		try:
			data = request.form.to_dict()
			write_to_csv(data)
			return redirect(url_for('index'))
		except:
			return 'Sorry, your message could not be saved to database.'
	else:
		return 'Something went wrong. Try again.'


if __name__ == '__main__':
	app.run(debug=True)
