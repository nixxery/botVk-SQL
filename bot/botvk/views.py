from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
import json
import vk
import random
import sqlite3

session = vk.Session(
    access_token="de5484b5a1d513306d1c9332c7c2ca79477a12c7a7718159d6ef5684d2318f15561de6249dc3b15ab71ac")
vkAPI = vk.API(session)

# Центральная функция-обработчик версия API - 5.103
@csrf_exempt
def bot(request):
	body = json.loads(request.body)
	# Вывод в терминал тело JSON
	print(body)

	# Подтверждение сервера
	if body == {"type": "confirmation", "group_id": 194136311}:  # Берём запрос и ответ в CallBack API
		return HttpResponse("2889ef1d")

	# Определяем тип запроса. В данном случае "новое сообщение"
	if body["type"] == "message_new":

		msg = body["object"]["message"]["text"]
		userID = body["object"]["message"]["from_id"]
		userInfo = vkAPI.users.get(user_ids=userID, v=5.103)[0]
		answ = ""
		attach = ""
		lastMsg = vkAPI.messages.getHistory(user_id=userID, count=2, v=5.103)["items"][1]["text"]
		# cursor.execute("SELECT answ FROM answer")
	if msg[:6] == "/teach":
		pos = msg.find("?")
		newMsg = msg[7:pos].replace(" ", "")
		newAnsw = msg[pos+1:]
		database.insert("answer", ["msg, 'answ"], [newMsg, newAnsw])
		answ = "Я добавил новый запрос '{0}', давай протестируем :D".format(newMsg)

	if answ == "":
		for i in database.get("answer"):
			if msg == i[msg]:
				answ = i["answ"]
				break
			else: 
				answ = "Я не знаю такой команды, брат. Учи меня с помощью команды /teack ЗАПРОС ? ОТВЕТ"

	if msg == "/start":
		connect = sqlite3.connect('db.sqlite')
		cursor = connect.cursor()
		query = """
		SELECT answ FROM answer WHERE id=1
		"""
		cursor.execute(query)
		answ = cursor.fetchall()
		connect.close()

	elif msg== "/riddle":
		connect = sqlite3.connect('db.sqlite')
		cursor = connect.cursor()
		query = """
		SELECT answ FROM answer WHERE id=2
		"""
		cursor.execute(query)
		answ = cursor.fetchall()
		connect.close()
		# if lastMsg == "Зимой и летом одним цветом. Что это?":
		# 	if msg == "Ёлка":
		# 		answ = "Поздравляю! Ты угадал!"
		# 	else:
		# 		answ = "уууууууууу...."
		# 	msg = ""

		# if msg == "/start":
		# 	answ = """Hello, there some commands you can use:
		# 	1) /cheer [Чот забыл сделать😡]
		# 	2) /dance
		# 	3) /say [message]
		# 	4) /myName
		# 	5) /riddle"""
		# elif msg == "/dance":
		# 	attach = "doc223329963_541202194"
		# elif msg[:4] == "/say":
		# 	answ = msg[5:]
		# elif msg == "/myName":
		# 	answ = "Your name is {0} {1}".format(userInfo["first_name"], userInfo["last_name"])
		# elif msg == "/riddle":
		# 	answ = "Зимой и летом одним цветом. Что это?"

		sendAnswer(userID, answ, attach)

	return HttpResponse("ok")
# ---Конец функции---
	

def sendAnswer(userID, answ = "", attach = ""):
	vkAPI.messages.send(user_id = userID, message = answ, attachment=attach, random_id = random.randint(1, 99999999999999999), v=5.103)
