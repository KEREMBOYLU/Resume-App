from django.shortcuts import render, redirect, get_object_or_404
from core.models import GeneralSetting, ImageSetting, Skill, Experience, Education, SocialMedia, Document

# Create your views here.

def get_general_setting(parameter):
    try:
        obj = GeneralSetting.objects.get(name=parameter).parameter
    except:
        obj = ''

    return obj

def get_image_setting(parameter):
    try:
        obj = ImageSetting.objects.get(name=parameter).file
    except:
        obj = ''

    return obj


def layout(request):
    site_title = get_general_setting('site_title')
    site_keywords = get_general_setting('site_keywords')
    site_description = get_general_setting('site_description')
    site_author = get_general_setting('site_author')
    home_banner_name = get_general_setting('home_banner_name')
    home_banner_title = get_general_setting('home_banner_title')
    home_banner_description = get_general_setting('home_banner_description')
    home_banner_birthdate = get_general_setting('home_banner_birthdate')
    home_banner_gsm = get_general_setting('home_banner_gsm')
    home_banner_telephone = get_general_setting('home_banner_telephone')
    home_banner_email = get_general_setting('home_banner_email')
    home_banner_location = get_general_setting('home_banner_location')
    about_myself_welcome = get_general_setting('about_myself_welcome')
    about_myself_footer = get_general_setting('about_myself_footer')

    # Images
    navbar_logo = get_image_setting('logo')
    favicon = get_image_setting('favicon')


    # Social Media
    social_medias = SocialMedia.objects.all().order_by('order')

    # Documents
    documents = Document.objects.all()

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

        'navbar_logo': navbar_logo,
        'favicon': favicon,

        'about_myself_welcome': about_myself_welcome,
        'about_myself_footer': about_myself_footer,

        'social_medias': social_medias,

        'documents': documents,
    }
    return context


def index(request):

    #İmages
    home_banner_photo = get_image_setting('home_banner_photo')

    # Skills
    skills = Skill.objects.all().order_by('order')

    # Experiences
    experiences = Experience.objects.all().order_by('-start_date')

    # Educations
    educations = Education.objects.all().order_by('-start_date')

    context = {

        'skills': skills,
        'experiences': experiences,
        'educations': educations,
        'home_banner_photo': home_banner_photo,

    }

    return render(request, 'index.html', context=context)


def redirect_urls(request, slug):
    doc = get_object_or_404(Document, slug=slug)
    return redirect(doc.file.url)
