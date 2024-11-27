from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings

# Function to send confirmation email
def send_confirmation_email(user_email, message_content):
    subject = 'Contact Us'
    message = message_content
    from_email = user_email
    recipient_list = ['markyleangela@gmail.com'] 
    
    send_mail(subject, message, from_email, recipient_list)

# View to handle contact form submission
def contact_view(request):
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        email = request.user.email
        message = request.POST.get('message')

        # Call the function to send the confirmation email
        send_confirmation_email(email, f"Name: {name}\nMessage: {message}")

        # After sending the email, you can redirect or show a success message
        return HttpResponse("Thank you for your message! We will get back to you shortly.")

    return render(request, 'contact.html')
