from django.shortcuts import redirect, render
from django.views.generic.list import ListView

from info_pages.models import *

# Create your views here.
class AboutUsView(ListView):
    def get(self, request): 
        about_us = AboutUs.objects.all().last()
        team = Team.objects.all()
        partners = Partners.objects.all()
        networks = SocialNetwork.objects.all()
        context = {
            'about_us':about_us, 
            'team':team, 
            'partners':partners,
            'networks': networks,
            'selected_nav_name': 'a_us'
        }
        return render(request, 'info_pages/about_us.html', context)
    

class WarantyView(ListView):
    def get(self, request): 
        waranties = Guarantees.objects.all()
        
        partners = Partners.objects.all()
        networks = SocialNetwork.objects.all()
        context = {
            'waranties':waranties, 
            'partners':partners,
            'networks': networks,
            'selected_nav_name': 'guaranties'
        }
        return render(request, 'info_pages/waranties.html', context)
    

class ContactsView(ListView):
    def get(self, request): 
        contact_info = ContactInfo.objects.all().first()
        
        partners = Partners.objects.all()
        networks = SocialNetwork.objects.all()
        context = {
            'contact_info':contact_info, 
            'partners':partners,
            'networks': networks,
            'selected_nav_name': 'contats'
        }
        return render(request, 'info_pages/contacts.html', context)
    
    
class LegalView(ListView):
    def get(self, request, pk): 
        legal =  LegalDocument.objects.get(id=pk)
        context = {
            'document':legal, 
            'selected_nav_name': 'legal'
        }
        return render(request, 'info_pages/legal.html', context)