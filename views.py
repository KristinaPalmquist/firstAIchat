from django.shortcuts import render, redirect
import ollama


def home(request):
    answer = None
    question = None
    if request.method == "POST":
        question = request.POST.get("question")
        try:
            response = ollama.chat(model='llama3.2', messages=[
                {
                    'role': 'user',
                    'content': question
                },
            ])
            print(response)
            answer = response.message.content
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
