from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
from google.genai import types
import webbrowser

import random 
import string
from .models import SharedSlides


import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

from google import genai

client = genai.Client()


# Create your views here.
def slide_builder(request):
    return render(request, 'slide_builder.html')

# _ at start means this function can be imported in any other file but it is intended for internal use in this file only. It is a convention to indicate that this function is a helper function and not meant to be used outside of this module.
def _make_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@csrf_exempt
def share_slides(request):
    if(request.method != 'POST'):
        return JsonResponse({'error': 'Only POST Allowed'}, status=405)

    try:
        body = json.loads(request.body.decode('utf-8'))
        slides = body.get('slides',[])
    except:
        return JsonResponse({'error':'Invalid Json'},status=400)
    code = _make_code()
    SharedSlides.objects.create(share_code=code,slides_json=slides)
    return JsonResponse({'code':code})
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

def _generate_slide_image(title:str , topic:str , type:str) -> str | None:
    prompt = (
        f"Create a slide of {type} style with illustrations talking about {topic}."
        f"The focus of this slide is: {title}. "
        "Minimal, clean, soft colours on a light background, no dense body text."
    )

    print("Generating image with prompt :",prompt)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=prompt,
            config = types.GenerateContentConfig(
                image_config = types.ImageConfig(
                    aspect_ratio="16:9",
                )
            )
        )

        print("Image generation response : ",response)

        for part in response.parts:
            if part.inline_data:
                image_bytes = part.inline_data.data # raw binary (01) data
                encoded = base64.b64encode(image_bytes).decode("ascii") # encode the 01 to string of text characters but still that b (b'iVBORw0KGgoAAAAN) Python still treats it as binary data. decode converts it to text removing b
                mime_type = part.inline_data.mime_type or "image/jpeg"
                data_url = f"data:{mime_type}; base64,{encoded}"
                print("Generated image data url: ", data_url[:80],"...")
                return data_url
    
    except Exception as e:
        print("Error in generate_slide_images :", e)
    
    return None
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
        image_url = _generate_slide_image(title,topic,slide_type)
        if image_url is None:
            image_url = ("https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&w=800&q=80")

        slides.append(
            {
                "id": idx,
                "title": title,
                "image": image_url,
            }
        )

    return JsonResponse({"slides": slides})

