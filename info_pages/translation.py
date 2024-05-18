from modeltranslation.translator import TranslationOptions, register
from info_pages.models import LegalDocument, Team, Partners, Guarantees, AboutUs, ContactInfo, SocialNetwork, PhoneNumber

@register(LegalDocument)
class LegalDocumentTranslationOptions(TranslationOptions):
    fields = ('name', 'text',)

@register(Team)
class TeamTranslationOptions(TranslationOptions):
    fields = ('name', 'position',)

@register(Partners)
class PartnersTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Guarantees)
class GuaranteesTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

@register(AboutUs)
class AboutUsTranslationOptions(TranslationOptions):
    fields = ('title', 'text',)


@register(PhoneNumber)
class PhoneNumberTranslationOptions(TranslationOptions):
    fields = ('phone_number',) 
