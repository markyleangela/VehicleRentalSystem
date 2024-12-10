from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from .forms import ContactForm

# Function to send confirmation email
def send_confirmation_email(user_email, message_content):
    subject = 'Contact Us'
    message = message_content
    from_email = 'markyleangela@gmail.com'
    recipient_list = [user_email] 
    
    send_mail(subject, message, from_email, recipient_list)

# View to handle contact form submission
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract form data
            
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Call the function to send the confirmation email
            send_confirmation_email(email, f"Name: {name}\nMessage: {message}")

            # After sending the email, redirect or show a success message
            return redirect('contact_view')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
