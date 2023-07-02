from django.shortcuts import render
from core.models import GeneralSetting,ImageSetting,Skill,Experience,Education

# Create your views here.

def index(request):
    site_title = GeneralSetting.objects.get(name='site_title').parameter
    site_keywords = GeneralSetting.objects.get(name='site_keywords').parameter
    site_description = GeneralSetting.objects.get(name='site_description').parameter
    site_author = GeneralSetting.objects.get(name='site_author').parameter

    home_banner_name = GeneralSetting.objects.get(name='home_banner_name').parameter
    home_banner_title = GeneralSetting.objects.get(name='home_banner_title').parameter
    home_banner_description = GeneralSetting.objects.get(name='home_banner_description').parameter
    home_banner_birthdate = GeneralSetting.objects.get(name='home_banner_birthdate').parameter
    home_banner_gsm = GeneralSetting.objects.get(name='home_banner_gsm').parameter
    home_banner_telephone = GeneralSetting.objects.get(name='home_banner_telephone').parameter
    home_banner_email = GeneralSetting.objects.get(name='home_banner_email').parameter
    home_banner_location = GeneralSetting.objects.get(name='home_banner_location').parameter

    about_myself_welcome = GeneralSetting.objects.get(name='about_myself_welcome').parameter
    about_myself_footer = GeneralSetting.objects.get(name='about_myself_footer').parameter


    #Images


    #Skills
    skills = Skill.objects.all().order_by('order')

    #Experiences
    experiences = Experience.objects.all().order_by('-start_date')

    #Educations
    educations = Education.objects.all().order_by('-start_date')




    context = {
    'site_title': site_title,
    'site_keywords': site_keywords,
    'site_description': site_description,
    'site_author': site_author,

    'home_banner_name': home_banner_name,
    'home_banner_title': home_banner_title,
    'home_banner_description': home_banner_description,
    'home_banner_birthdate': home_banner_birthdate,
    'home_banner_gsm': home_banner_gsm,
    'home_banner_telephone': home_banner_telephone,
    'home_banner_email': home_banner_email,
    'home_banner_location': home_banner_location,

    'about_myself_welcome': about_myself_welcome,
    'about_myself_footer': about_myself_footer,

    'skills': skills,
    'experiences': experiences,
    'educations': educations,

    }

    return render(request, 'index.html', context=context)

