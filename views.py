from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
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
            
            # Temporary fallback for Azure deployment issues
            if not api_key:
                # Try direct assignment as fallback
                api_key = 'AIzaSyCICm-GlUy4SZOgYas-gj4ISDJuJtg3jfM'
                print("WARNING: Using fallback API key - fix Azure env vars")
            
            if not api_key:
                answer = ("Sorry, the AI service is not configured yet. "
                          "Please set GEMINI_API_KEY environment variable.")
            else:
                genai.configure(api_key=api_key)
                
                # Create the model
                model = genai.GenerativeModel('gemini-flash-latest')
                
                # Generate response
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
    
    # Get environment variables with debugging info
    secret_key = os.getenv('SECRET_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    status = {
        'status': 'ok',
        'django_version': django.get_version(),
        'secret_key_set': bool(secret_key),
        'secret_key_length': len(secret_key) if secret_key else 0,
        'secret_key_preview': (secret_key[:10] + '...'
                               if secret_key else None),
        'gemini_key_set': bool(gemini_key),
        'gemini_key_length': len(gemini_key) if gemini_key else 0,
        'gemini_key_preview': (gemini_key[:15] + '...'
                               if gemini_key else None),
        'debug_mode': settings.DEBUG,
        'allowed_hosts': settings.ALLOWED_HOSTS,
        'csrf_trusted_origins': getattr(settings, 'CSRF_TRUSTED_ORIGINS', []),
        'request_scheme': request.scheme,
        'request_host': request.get_host(),
        'all_env_vars': list(os.environ.keys()),  # Show all available env vars
    }
    from django.http import JsonResponse
    return JsonResponse(status)
