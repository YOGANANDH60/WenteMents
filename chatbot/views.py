from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from shopifyyyy.models import *
@csrf_exempt  # TEMPORARY: Disables CSRF protection (Only for debugging)
def chatbot_response(request):
    if request.method == "POST":
        user_input = request.POST.get("message", "").lower()
        categories = category.objects.filter(status=0)

                # Define keyword-based product links
        product_links = {
             "outfit": reverse("category"), 
            "Accessories": reverse("category"),
            "accessories": reverse("category"),
            "Sports":reverse("category"),
            "sports":reverse("category"),
            "Games": reverse("category"),
            "games": reverse("category"),
            "Electronics": reverse("category"),
            "electronics": reverse("category"),
        }

        # Check if input matches a product
        for keyword, link in product_links.items():
            if keyword in user_input:
                response_text = f"Click here to check {keyword}: <a href='{link}' target='_blank'>{link}</a>"
                return JsonResponse({"response": response_text,})

        responses = {
            "hi": "Hello! How can I assist you?",
            "hello": "Hi there! What can I do for you?",
            "how are you": "I'm just a bot, but I'm doing great! How about you?",
            "what is your name": "I'm wentment's chatbot!",
            "bye": "Goodbye! Have a great day!",
            "who you are": "I'm wentment's chatbot! How can I help you?",
            "category": "We have a <li>outfit</li><li>Accessories</li><li>Sports</li><li>Games</li><li>Electronics</li> of categories. What are you looking for?",
        }

        response_text = responses.get(user_input, "I'm not sure how to respond to that.")
        return JsonResponse({"response": response_text })

    # Return chatbot.html if it's a GET request
    return render(request, "chatbot/chatbot.html")
