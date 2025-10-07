from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai  # type: ignore
import os


@csrf_exempt  # Temporary: Remove this once CSRF is working
def home(request):
    answer = None
    question = None
    if request.method == "POST":
        question = request.POST.get("question")
        try:
            # Configure Gemini API
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                answer = ("Sorry, the AI is not at home. "
                          "Please come back later.")
            else:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-flash-latest')
                response = model.generate_content(question)
                answer = response.text

            request.session['answer'] = answer
            request.session['question'] = question
            return redirect('home')
        except Exception as e:
            answer = f"Error: {e}"

    # Retrieve and clear from session after redirect
    if 'answer' in request.session:
        answer = request.session.pop('answer')
    if 'question' in request.session:
        question = request.session.pop('question')

    return render(request, "home.html", {
        "answer": answer,
        "question": question
        })


def health_check(request):
    """Simple health check endpoint for Azure diagnostics"""
    import django
    from django.conf import settings
    
    # Get environment variables - NO sensitive data exposed
    secret_key = os.getenv('SECRET_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    status = {
        'status': 'ok',
        'django_version': django.get_version(),
        'secret_key_configured': bool(secret_key),
        'gemini_key_configured': bool(gemini_key),
        'debug_mode': settings.DEBUG,
        'allowed_hosts': settings.ALLOWED_HOSTS,
        'csrf_trusted_origins': getattr(settings, 'CSRF_TRUSTED_ORIGINS', []),
        'request_scheme': request.scheme,
        'request_host': request.get_host(),
    }
    from django.http import JsonResponse
    return JsonResponse(status)
