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
	

	if body == {"type": "confirmation", "group_id": 194136311}:
		return HttpResponse("095637fd")

	if body["type"] == "message_new":
		msg = body["object"]["message"]["text"]
		payload = body["object"]["message"]["payload"]
		userID = body["object"]["message"]["from_id"]
		userInfo = vkAPI.users.get(user_ids=userID, v=5.103)[0]
		answ = ""
		attach = ""

	if payload == """{"command":"start"}""":
		keyboardStart(request, userID)	

		# if msg[:6] == "/teach":
		# 	pos = msg.find("?")
		# 	newMsg = msg[7:pos].replace(" ", "")
		# 	newAnsw = msg[pos+1:]
		# 	database.insert("answer", ["msg", "answ"], [newMsg, newAnsw])
		# 	answ = "Я добавил новый запрос '{0}', давай тестить".format(newMsg)

		# if answ == "":
		# 	for i in database.get("answer"):
		# 		if msg == i["msg"]:
		# 			answ = i["answ"]
		# 			break
		# 		else:
		# 			answ = database.get("answer")

		# sendAnswer(userID, answ, attach)

		return HttpResponse("ok")


def keyboardStart(request, userID):
	answ = "Привет! Выбери свою группу"
	keyboard = json.dumps ({
		"one_time": True,
		"buttons":[[
			{
				"action":{
					"type":"text",
					"label":"Администратор",
					"payload":"""{"command":"start"}"""
				},
				"color":"negative"
			},
			{
				"action":{
					"type":"text",
					"label":"Пользователь",
					"payload":"""{"command":"start"}"""
				},
				"color":"primary"
			},
				{
				"action":{
					"type":"text",
					"label":"Ученик",
					"payload":"""{"command":"start"}"""
				},
				"color":"positive"
			}	
		]]
	})

	sendMessage(userID, answ, keyboard = keyboard)

# def sendAnswer(userID="", answ="", attach=""):
#     vkAPI.messages.send(user_id=userID, message=answ, attachment=attach, random_id=random.randint(1, 99999999999999999), v=5.103)

	
def sendMessage(userID="", msg="", attachment="", keyboard=""):
	vkAPI.messages.send(user_id=userID, message=msg, keyboard=keyboard, random_id=random.randint(1, 99999999999999999), v=5.103)

# ===============================================================================================================================

lg = {
	"success": False,
	"groups": []
}

def login(request):
	global lg

	tmp = []
	for i in database.get("groups"):
		tmp.append(i["groupName"])

	lg["groups"] = tmp

	if ("login_" and "password") in request.GET:
		if "admin" == request.GET.get("login") and "0000" == request.GET.get("password"):
			lg["success"] = True

	print(lg)
	
	return render(request, "login.html", lg)