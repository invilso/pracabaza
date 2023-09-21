# myapp/context_processors.py

from info_pages.models import LegalDocument, SocialNetwork

def legal_docs(request):
    legals = LegalDocument.objects.all()
    return {'legals': legals}

def socials_footer(request):
    socials_footer = SocialNetwork.objects.all()
    return {'socials_footer': socials_footer}