from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import openai


openai.api_key = 
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
        raw_message = data.get("message", "")
        
        if "Si" in raw_message or "Al" in raw_message or "O" in raw_message:
            frame = raw_message.split("프레임")[1].split("의")[0].strip() if "프레임" in raw_message else "?"
            system_prompt = (
                "너는 반도체 공정을 설명하는 AI야. "
                "사용자가 보내는 xyz 구조는 반도체 공정 중에 시뮬레이션된 원자 위치를 나타내는 자료야. "
                "구조 속 원자들의 상대적 거리, 배열, 상호작용을 기반으로 반응이 일어나고 있는지 추론해줘. "
                "가능하다면 흡착, 탈착, 결합 생성, 산화, 재배열 등의 공정 용어를 사용해서 설명해줘. "
                "초보자도 이해할 수 있게 쉽게 설명해줘."
            )

            # 너무 긴 경우 자름
            if len(raw_message) > 3000:
                raw_message = raw_message[:3000] + "\n\n(구조가 길어 생략됨)"

            user_prompt = f"""
[프레임 {frame}]의 xyz 구조입니다.

<구조 시작>
{raw_message}
<구조 끝>

이 구조에서 어떤 반응이 일어나는 것으로 보이나요?
특히 표면에서의 결합, 이동, 변화, 상호작용 양상을 물리화학적으로 설명해주세요.
"""

        else:
            system_prompt = "너는 반도체 공정 튜터야. 학생의 질문에 친절하게 답해줘."
            user_prompt = raw_message

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # gpt-4로 바꿔도 좋음
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        reply = response.choices[0].message.content.strip()
        return JsonResponse({"reply": reply})
