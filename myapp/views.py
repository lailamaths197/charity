from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DonationForm
from .forms import VolunteerForm

def home_view(request):
    return render(request, 'home.html')
def about_page(request):
    # Defining core content statically matching your Figma layout cards
    values = [
        {"title": "Compassion","icon": "bi-heart-fill", "desc": "We approach our work with empathy and understanding, recognizing the inherent dignity of every person."},
        {"title": "Collaboration", "icon": "bi-people-fill", "desc": "We believe in the power of partnerships and collective action to achieve lasting change."},
        {"title": "Integrity", "icon": "bi-shield-check", "desc": "We uphold the highest standards of honesty and ethical conduct in all our endeavors."}
    ]
    
    team_members = [
        {"name": "Sarah Johnson", "role": "Co-Founder & Executive Director", "image": "images/chimg10.png"},
        {"name": "David Lee", "role": "Co-Founder & Program Director", "image": "images/chimg11.png"},
        {"name": "Emily Carter", "role": "Volunteer Coordinator", "image": "images/chimg12.png"}
    ]
    
    return render(request, 'about.html', {'values': values, 'team_members': team_members})

def causes_page(request):
    # Pure static rendering with no database overhead
    return render(request, 'causes.html')    




def donate_page(request):
    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            # Store necessary data in session to personalize the thank-you screen
            request.session['donor_name'] = form.cleaned_data['name']
            request.session['donation_amount'] = form.cleaned_data['amount']
            return redirect('donate_success') # Redirects safely to success view
    else:
        form = DonationForm()
        
    return render(request, 'donate.html', {'form': form})

def donate_success(request):
    # Fetch session tokens with safe fallback text if accessed directly
    context = {
        'donor_name': request.session.get('donor_name', 'Generous Supporter'),
        'amount': request.session.get('donation_amount', 'your chosen amount')
    }
    return render(request, 'donate_success.html', context)

def contact_page(request):
    return render(request, 'contact.html')


def volunteer_page(request):
    if request.method == "POST":
        form = VolunteerForm(request.POST)
        if form.is_valid():
            messages.success(request, "Thank you for applying! Our team will contact you soon.")
            return redirect('volunteer_page')
    else:
        form = VolunteerForm()
    return render(request, 'volunteer.html', {'form': form})            