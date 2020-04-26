from django.views.decorators.csrf import csrf_exempt 
from django.http import HttpResponse
from django.shortcuts import render
import json, vk, random

# Создаём сессию по своему ключу
session = vk.Session(access_token="de5484b5a1d513306d1c9332c7c2ca79477a12c7a7718159d6ef5684d2318f15561de6249dc3b15ab71ac")
vkAPI = vk.API(session)

@csrf_exempt
def bot(request):
	body = json.loads(request.body)
	print(body)
	if body == { "type": "confirmation", "group_id": 194136311 }:
		return HttpResponse("2889ef1d")
	if body["type"] == "message_new": 
		userID = body["object"]["message"]["from_id"]
		if body["object"]["message"]["text"] == "Привет":
			msg = "Привет, я ничего не умею"
			vkAPI.messages.send(user_id = userID, message = msg, random_id = random.randint(1, 99999999999999999), v=5.103)
	return HttpResponse("ok")

