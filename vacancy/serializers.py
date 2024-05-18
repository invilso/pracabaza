from rest_framework import serializers
from .models import Vacancy, City, State, Photo, Video, InfoLabel, HourlyPaymentOption, WorkDuty, Requirement, Sex, Category, Index, View, Salary

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class InfoLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoLabel
        fields = '__all__'

class HourlyPaymentOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HourlyPaymentOption
        fields = '__all__'

class WorkDutySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkDuty
        fields = '__all__'

class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = '__all__'

class SexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sex
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Index
        fields = '__all__'

class ViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = View
        fields = '__all__'

class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = '__all__'

class VacancySerializer(serializers.ModelSerializer):
    city = CitySerializer()
    state = StateSerializer()
    card_photo = PhotoSerializer()
    photos = PhotoSerializer(many=True)
    video = VideoSerializer()
    info_label = InfoLabelSerializer()
    salary_per_hour = HourlyPaymentOptionSerializer(many=True)
    work_duties = WorkDutySerializer(many=True)
    requirements = RequirementSerializer(many=True)
    sex = SexSerializer(many=True)
    category = CategorySerializer()
    index = IndexSerializer()

    class Meta:
        model = Vacancy
        fields = '__all__'
