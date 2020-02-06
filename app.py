from flask import Flask, render_template, url_for, flash, request, redirect, send_from_directory
import csv

app = Flask(__name__)

app.config.update(dict(SECRET_KEY='d1e6b983ae53474d2df0d3d381ef05a3'))

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
		'question': 'What is and integer?',
		'pos_answers': ['Whole number', 'Word', 'Sentence'],
		'correct_answer': 'Whole number'
	},
]


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		points = 0
		answers = request.form

		for pnr, ans in answers.items():
			if ans == DATA[int(pnr)]['correct_answer']:
				points += 1
		flash("Your result: {0}, congrats 😁".format(points))
		return redirect(url_for('index'))

	return render_template('index.html', questions=DATA)


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
