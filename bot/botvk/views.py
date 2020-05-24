from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
import json
import vk
import random
import sqlite3
import database

# Создаём сессию по своему ключу
session = vk.Session(access_token="de5484b5a1d513306d1c9332c7c2ca79477a12c7a7718159d6ef5684d2318f15561de6249dc3b15ab71ac")
vkAPI = vk.API(session)


@csrf_exempt
def bot(request):
	body = json.loads(request.body)
	print(body)

	if body == { "type": "confirmation", "group_id": 194136311 }:
		return HttpResponse("3fd765a5")


	if body["type"] == "message_new":
		msg = body["object"]["message"]["text"]
		userID = body["object"]["message"]["from_id"]
		userInfo = vkAPI.users.get(user_ids = userID, v=5.103)[0]
		
		if "payload" in body["object"]["message"]:
			payload = body["object"]["message"]["payload"]
			if payload == """{"command":"start"}""":
				keyboardStart(request, userID)
			else:
				try:
					gpid = -1
					gpname = ""
					if payload == """{"command":"admin"}""":
						gpid = str(1)
						gpname = "Администратор"
					elif payload == """{"command":"mentor"}""":
						gpid = str(2)
						gpname = "Наставник"
					elif payload == """{"command":"student"}""":
						gpid = str(3)
						gpname = "Ученик"
					database.insert("user", ["id, groupId"], [str(userID), gpid])
					speak(request,userID, userInfo, answ = "Вы были добавлены в группу {0}".format(gpname))
				except Exception as e:
					speak(request,userID, userInfo, answ = "Ошибка")
		else:
			speak(request,userID, userInfo, msg)

	return HttpResponse("ok")

def sendAnswer(userID, answ = "", attach = "", keyboard = json.dumps({"buttons":[],"one_time":True})):
	vkAPI.messages.send(user_id = userID, message = answ, attachment=attach, keyboard=keyboard, random_id = random.randint(1, 99999999999999999), v=5.103)

def speak(request,userID, userInfo = "", msg = "",  answ = "", attach=""):
	if msg[:6] == "/teach":
		pos = msg.find("?")
		newMsg = msg[7:pos].replace(" ", "")
		newAnsw = msg[pos+1:]
		database.insert("answer", ["msg", "answ"], [newMsg, newAnsw])
		answ = "Я добавил новый запрос '{0}', давай попробуем".format(newMsg)
	elif msg == "/list":
		answ = database.get("answer", ["msg"])
	elif msg == "/whoAmI":
		answ = """Вы относитесь к группе {0}""".format(database.getGroup(str(userID))[0]["groupName"])
	elif msg == "/whoAreThey":
		answ = """Пользователи:\n"""
		for i in database.getGroup():
			answ += """id: {0}, group: {1}\n""".format(i["id"], i["groupName"])


	if answ == "":
		for i in database.get("answer"):
			if msg == i["msg"]:
				answ = i["answ"]					
				break
			else:
				answ = "Я не знаю такой команды. Можешь научить меня используя команду /teach ЗАПРОС ? ОТВЕТ"

	sendAnswer(userID, answ, attach)

def keyboardStart(request, userID):
	answ = "Привет! Выбери свою группу пользователя!"
	keyboard = json.dumps({
		"one_time": True,
		"buttons":[[
			{
				"action": {
					"type":"text",
					"label":"Admin",
					"payload": """{"command":"admin"}"""
				},
				"color":"negative"
			},
			{
				"action": {
					"type":"text",
					"label":"Student",
					"payload": """{"command":"mentor"}"""
				},
				"color":"positive"
			},
			{
				"action": {
					"type":"text",
					"label":"User",
					"payload": """{"command":"student"}"""
				},
				"color":"primary"
			}
		]]
	})
	sendAnswer(userID, answ, keyboard = keyboard)





# ========================================================================================================================

# Рендер нашей страницы login.html

lg = {
	"success": False,
	"groups": database.get("groups")
}
@csrf_exempt
def login(request):
	global lg
	print(lg)


	if request.method == "POST":
		if request.POST.get("login") == "admin" and request.POST.get("password") == "0000":
			lg["success"] = True
		elif (request.POST.get("message") and request.POST.get("group")) != None:
			for user in database.getGroup(groupID = request.POST.get("group")):
				sendAnswer(user["id"], answ = request.POST.get("message"))
		
	return render(request, "login.html", lg)
