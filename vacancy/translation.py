from modeltranslation.translator import TranslationOptions, register
from .models import Category, Vacancy, HourlyPaymentOption, Requirement, WorkDuty, InfoLabel, Sex, City, State

@register(Vacancy)
class VacancyTranslationOptions(TranslationOptions):
    fields = ('name', 'title', 'description', 'work_schedule')

@register(HourlyPaymentOption)
class HourlyPaymentOptionTranslationOptions(TranslationOptions):
    fields = ('payment_type',)

@register(Requirement)
class RequirementTranslationOptions(TranslationOptions):
    fields = ('description',)

@register(WorkDuty)
class WorkDutyTranslationOptions(TranslationOptions):
    fields = ('description',)

@register(InfoLabel)
class InfoLabelTranslationOptions(TranslationOptions):
    fields = ('house', 'benefits')

@register(Sex)
class SexTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(State)
class StateTranslationOptions(TranslationOptions):
    fields = ('name',)
    
@register(Category)
class StateTranslationOptions(TranslationOptions):
    fields = ('name',)
