import requests
import json
import html
import random
import time
print("Welcome to Trivia!")
correct_input =  False
input_string = "Number of questions you want to answer (max: 10): "
while correct_input == False:
	try:
		ch = int(input(input_string))
	except ValueError:
		print('Please enter a correct value!\n')
		continue
	if ch<=10 and ch> 0:
		correct_input = True
	else:
		print('Please choose up to 10 questions\n')
question_number = ch
category_ids_temp = requests.get('https://opentdb.com/api_category.php')
category_ids_temp = json.loads(category_ids_temp.text)
category_ids = category_ids_temp["trivia_categories"]
input_string = 'Enter the number for your choice: \n\n'
for i in range(1, len(category_ids)+1):
	input_string += str(i) + ") " + category_ids[i-1]["name"] + "\n"
correct_input =  False
input_string += "\nYour choice: "
print("\n")
while correct_input == False:
	try:
		ch = int(input(input_string))
	except ValueError:
		print('Please enter a correct value!\n')
		continue
	if ch<=(len(category_ids)+1) and ch> 0:
		correct_input = True
	else:
		print('Please choose 1, 2, 3 etc.\n')
category_id_ch = category_ids[ch-1]['id']
print("You have chosen " + category_ids[ch-1]['name'])

correct_input =  False
input_string = "Choose a difficulty:\n1) Easy\n2) Medium\n3) Difficult\nYour choice: "
difficulty = {1 : "easy", 2: "medium", 3: "hard"}
while correct_input == False:
	try:
		ch = int(input(input_string))
	except ValueError:
		print('Please enter 1, 2 or 3\n')
		continue
	if ch<=3 and ch> 0:
		correct_input = True
	else:
		print('Please enter 1, 2 or 3\n')
difficulty_ch = ch

check_questions = requests.get("https://opentdb.com/api_count.php?category=" + str(category_id_ch))
check_questions = json.loads(check_questions.text)
available_question_number = check_questions["category_question_count"]["total_" + difficulty[difficulty_ch] + "_question_count"]

request_questions = json.loads(requests.get("https://opentdb.com/api.php?amount=" + str(available_question_number) + "&category=" + str(category_id_ch) + "&difficulty=" + difficulty[difficulty_ch]).text)
request_questions = request_questions["results"]

available_question_number = len(request_questions)

if available_question_number==0:
	print("No questions in this category available")
	quit()
if available_question_number<question_number:
	print("Only " + str(available_question_number) + " questions available\n")
	question_number = available_question_number
# print("https://opentdb.com/api.php?amount=" + str(question_number) + "&category=" + str(category_id_ch) + "&difficulty=" + difficulty[difficulty_ch])
# print(request_questions)
random.shuffle(request_questions)
questions_answered = 1
question_indexes = []
score = 0
print("\n\n")
while questions_answered<=question_number:
	question_string = ""
	print("Question " + str(questions_answered) + " of " + str(question_number) + ":")
	rand_question_index = random.randint(0, available_question_number-1)
	while rand_question_index in question_indexes:
	    rand_question_index = random.randint(0, available_question_number-1)
	# print(rand_question_index)
	# print(available_question_number)
	question_indexes.append(rand_question_index)
	current_question = request_questions[rand_question_index]
# 	print(current_question["incorrect_answers"])
	answers = current_question["incorrect_answers"]
	answers.append(current_question["correct_answer"])
	# print(answers)
	random.shuffle(answers)
	question_string = html.unescape(current_question["question"]) + "\n\n"
	for i in range(1,len(answers)+1):
	    question_string += str(i) + ") " + html.unescape(answers[i-1]) + "\n"
	print(question_string)
	correct_input =  False
	input_string = "Your answer: "
	while correct_input == False:
	    try:
	        ch = int(input(input_string))
	    except ValueError:
	        print('Please enter the number for the choice!\n')
	        continue
	    if ch<=len(answers) and ch> 0:
	        correct_input = True
	    else:
	        print('Please enter a number between 1-' + str(len(answers)) + '\n')
	user_answer = ch
	if current_question["correct_answer"] == answers[user_answer-1]:
		print("Correct Answer!\n\n")
		score += 1
	else:
	    print("Incorrect Answer! The correct answer was '" + current_question["correct_answer"] + "'\n")
	questions_answered += 1
	time.sleep(1.5)
print("You scored " + str(score) + " on " + str(question_number))

















