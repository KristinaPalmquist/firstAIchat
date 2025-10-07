from django.shortcuts import render, redirect
import google.generativeai as genai
import os


def home(request):
    answer = None
    question = None
    if request.method == "POST":
        question = request.POST.get("question")
        try:
            # Configure Gemini API
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise Exception("GEMINI_API_KEY environment variable not set!")
            
            genai.configure(api_key=api_key)
            
            # Create the model
            model = genai.GenerativeModel('gemini-1.5-flash')
            
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
