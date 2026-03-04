from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

from google import genai

client = genai.Client()


# Create your views here.
def slide_builder(request):
    return render(request, 'slide_builder.html')


def _generate_slide_titles(topic: str, slide_type: str) -> list[str]:
    prompt = f"""
        Return exactly five slide titles for a beginner-friendly {slide_type} presentation about "{topic}".
        Must return only valid JSON in this exact structure:
        {{
            "slides":[
                {{"title":"..."}},
                {{"title":"..."}},
                {{"title":"..."}},
                {{"title":"..."}},
                {{"title":"..."}}
            ]
        }}
    """

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[{"text": prompt}],
        )

        raw = ""
        for part in response.parts:
            if part.text:
                raw += part.text.strip()

        print("Raw title generation response:", raw)
        data = json.loads(raw)
        titles = [s["title"] for s in data.get("slides", []) if "title" in s]

        if len(titles) == 5:
            return titles

    except Exception as e:
        print("Title generation failed:", e)

    return [
        f"Introduction to {topic}",
        f"Core ideas of {topic}",
        f"How {topic} works",
        f"Use case of {topic}",
        f"Future of {topic}",
    ]


@csrf_exempt
def generate_slides(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST Allowed'}, status=405)

    try:
        body = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    topic = body.get('topic', '').strip()
    slide_type = body.get('slide_type', '').strip()

    if not topic:
        topic = 'Random Topic'

    if not slide_type:
        slide_type = 'General'

    titles = _generate_slide_titles(topic, slide_type)
    print("Titles from AI:", titles)

    slides = []
    for idx, title in enumerate(titles):
        slides.append(
            {
                "id": idx,
                "title": title,
                "image": "https://pin.it/17N10Xb2V",
            }
        )

    return JsonResponse({"slides": slides})
