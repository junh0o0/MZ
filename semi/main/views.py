from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import openai


openai.api_key = 
# Create your views here.
def index(request):
    return render(request,'main/index.html')

def oxidation(request):
    return render(request, 'main/oxidation.html')

def photo(request):
    return render(request, 'main/photo.html')

def etching(request):
    return render(request, 'main/etching.html')

def deposition(request):
    return render(request, 'main/deposition.html')

@csrf_exempt
def ai_chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message", "")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "너는 반도체 공정을 친절히 설명하는 도우미야."},
                {"role": "user", "content": message}
            ]
        )

        reply = response.choices[0].message.content.strip()
        return JsonResponse({"reply": reply})
