from django.shortcuts import get_object_or_404, render, redirect
from .forms import ContactForm
from .models import Contact, PortfolioItem
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import smtplib
from django.contrib import messages
from .utils.brevo_email import send_brevo_email
# from supabase import create_client, Client
# import os

# Create your views here.

# def home(request):
#     return render(request, 'index.html')

def home(request):
    portfolio_items = PortfolioItem.objects.all()[:6]  # Show first 6 items on homepage
    return render(request, 'index.html', {'portfolio_items': portfolio_items})

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def team(request):
    return render(request, 'team.html')

def contact(request):
    return render(request, 'contact.html')

# def contact_view(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('success_page')  # Redirect to a success page
#     else:
#         form = ContactForm()
    
#     return render(request, 'index.html', {'form': form})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                form.save()

                # Prepare email content
                # context = {
                #     'user_name': form.cleaned_data.get('name', 'there'),
                #     'calendly_link': settings.CALENDLY_LINK,
                #     'company_name': 'OneSas'
                # }
                
                # # Create email
                # email = EmailMultiAlternatives(
                #     subject=f"Schedule your OneSas meeting",
                #     body=f"Hi {context['user_name']}, book here: {context['calendly_link']}",
                #     from_email=f"OneSas Support <{settings.DEFAULT_FROM_EMAIL}>",
                #     to=[form.cleaned_data['email']],
                #     reply_to=["abdulhanan7900@gmail.com"],
                # )
                
                # # Attach HTML version
                # html_content = render_to_string('emails/meeting_invitation.html', context)
                # email.attach_alternative(html_content, "text/html")
                
                # # Send email
                # email.send()
                
                # Prepare email context
                # calendly_link = 'https://calendly.com/yourusername'
                # context = {
                #     'user_name': form.cleaned_data.get('name', 'there'),
                #     'calendly_link': settings.CALENDLY_LINK,
                #     'company_name': 'OneSas'
                # }
                
                # # Render both text and HTML versions
                # text_content = f"""
                # Hi {context['user_name']},
                
                # Thank you for contacting {context['company_name']}!
                
                # Please schedule a meeting at: {settings.CALENDLY_LINK}
                
                # Best regards,
                # The {context['company_name']} Team
                # """
                
                # html_content = render_to_string('emails/meeting_invitation.html', context)
                
                # # Create email
                # msg = EmailMultiAlternatives(
                #     subject=f"Schedule your OneSas meeting with {context['user_name']}",
                #     body=text_content,
                #     from_email=settings.DEFAULT_FROM_EMAIL,  # Use a branded from address
                #     to=[form.cleaned_data['email']],
                #     headers={
                #         'List-Unsubscribe': '<mailto:unsubscribe@onesas.com>, <https://onesas.com/unsubscribe>',
                #         'X-Mailer': 'OneSasApp',
                #         'X-Priority': '1',
                #     }
                # )
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()

                context = {
                    'user_name': form.cleaned_data.get('name', 'there'),
                    'calendly_link': settings.CALENDLY_LINK,
                    'company_name': 'OneSas'
                }
                
                # Render HTML template
                html_content = render_to_string('emails/meeting_invitation.html', context)
                
                # Send via Brevo API
                send_brevo_email(
                    to_email=form.cleaned_data['email'],
                    subject=f"Schedule your OneSas meeting",
                    html_content=html_content
                )

                return JsonResponse({'success': True, 'message': 'Your message has been sent successfully! You had received an email from Us! Check your Inbox and Spam'})
            except smtplib.SMTPAuthenticationError:
                messages.error(request, "Failed to send email. Please contact support.")
                # Log this error for admin to check credentials
                
            except Exception as e:
                messages.error(request, "There was an error sending your message. Please try again later.")
                # Log the full error for debugging
                print(f"Email sending error: {str(e)}")
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ContactForm()
    return render(request, 'index.html', {'form': form})

def success_page(request):
    return render(request, 'success.html')

def portfolio_list(request):
    items = PortfolioItem.objects.all().order_by('-project_date')
    return render(request, 'portfolio/portfolio.html', {'portfolio_items': items})

# def portfolio_detail(request, pk):
#     item = get_object_or_404(PortfolioItem, pk=pk)
#     return render(request, 'portfolio/portfolio-details.html', {'portfolio_item': item})

def portfolio_detail(request, slug):
    item = get_object_or_404(PortfolioItem, slug=slug)
    return render(request, 'portfolio/portfolio-details.html', {'portfolio_item': item})

def service_detail(request, slug):
    # You'll need to create a Service model or use some way to identify services
    # For now, we'll just pass the slug to the template
    context = {
        'slug': slug,
        'service_name': slug.replace('-', ' ').title(),
    }
    return render(request, 'services-details.html', context)

# def upload_to_supabase(file, file_path):
#     supabase_url = os.getenv('SUPABASE_URL')
#     supabase_key = os.getenv('SUPABASE_KEY')
#     supabase: Client = create_client(supabase_url, supabase_key)
    
#     # Upload file to Supabase storage
#     response = supabase.storage.from_('one-sas').upload(
#         file_path, 
#         file.read(),
#         {"content-type": file.content_type}
#     )
#     return response