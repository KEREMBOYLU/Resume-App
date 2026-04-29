from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from core.models import GeneralSetting, ImageSetting, Skill, Experience, Education, SocialMedia, Document, SitePreference
from projects.models import Project


def get_general_setting_text(parameter):
    try:
        return GeneralSetting.objects.get(name=parameter).text_parameter
    except GeneralSetting.DoesNotExist:
        return ''


def get_general_setting(parameter):
    try:
        return GeneralSetting.objects.get(name=parameter).parameter
    except GeneralSetting.DoesNotExist:
        return ''


def get_image_setting(parameter):
    try:
        return ImageSetting.objects.get(name=parameter).file
    except ImageSetting.DoesNotExist:
        return ''


def get_general_settings_map():
    settings = GeneralSetting.objects.all().values('name', 'parameter', 'text_parameter')
    return {
        setting['name']: setting['text_parameter'] or setting['parameter'] or ''
        for setting in settings
    }


def get_site_preference():
    preference = SitePreference.objects.first()
    if preference:
        return preference
    return SitePreference(default_journey_tab=SitePreference.JourneyTab.EDUCATION)


def layout(request):
    context = {
        'gs': get_general_settings_map(),
        'site_title': get_general_setting('site_title'),
        'site_keywords': get_general_setting('site_keywords'),
        'site_description': get_general_setting('site_description'),
        'site_author': get_general_setting('site_author'),
        'site_brand_short': get_general_setting('site_brand_short'),
        'site_nav_cv_label': get_general_setting('site_nav_cv_label'),
        'site_footer_brand': get_general_setting('site_footer_brand'),
        'site_footer_copyright': get_general_setting('site_footer_copyright'),
        'favicon': get_image_setting('favicon'),
        'social_medias': SocialMedia.objects.all().order_by('order'),
        'documents': Document.objects.all().order_by('order'),
        'public_site_origin': settings.PUBLIC_SITE_ORIGIN,
    }
    return context


def index(request):
    site_preference = get_site_preference()
    context = layout(request)
    context.update({
        'page_title': context.get('site_title') or 'Home',
        'home_hero_profile_image': get_image_setting('home_hero_profile_image'),
        'home_hero_profile_alt': get_general_setting('home_hero_profile_alt'),
        'home_hero_greeting': get_general_setting('home_hero_greeting'),
        'home_hero_role': get_general_setting('home_hero_role'),
        'home_hero_passion': get_general_setting('home_hero_passion'),
        'home_hero_location': get_general_setting('home_hero_location'),
        'home_hero_contact_email': get_general_setting('home_hero_contact_email'),
        'home_hero_cta_contact_url': get_general_setting('home_hero_cta_contact_url'),
        'home_hero_cta_contact_label': get_general_setting('home_hero_cta_contact_label'),
        'home_hero_cta_github_url': get_general_setting('home_hero_cta_github_url'),
        'home_hero_cta_github_label': get_general_setting('home_hero_cta_github_label'),
        'home_hero_cta_linkedin_url': get_general_setting('home_hero_cta_linkedin_url'),
        'home_hero_cta_linkedin_label': get_general_setting('home_hero_cta_linkedin_label'),
        'home_about_heading': get_general_setting('home_about_heading'),
        'home_about_subtitle': get_general_setting('home_about_subtitle'),
        'home_about_paragraph_1': get_general_setting_text('home_about_paragraph_1'),
        'home_about_paragraph_2': get_general_setting_text('home_about_paragraph_2'),
        'home_stack_heading': get_general_setting('home_stack_heading'),
        'home_journey_exp_1_company': get_general_setting('home_journey_exp_1_company'),
        'home_journey_exp_1_period': get_general_setting('home_journey_exp_1_period'),
        'home_journey_exp_1_desc': get_general_setting('home_journey_exp_1_desc'),
        'home_journey_exp_2_company': get_general_setting('home_journey_exp_2_company'),
        'home_journey_exp_2_period': get_general_setting('home_journey_exp_2_period'),
        'home_journey_exp_2_desc': get_general_setting('home_journey_exp_2_desc'),
        'home_journey_edu_1_school': get_general_setting('home_journey_edu_1_school'),
        'home_journey_edu_1_period': get_general_setting('home_journey_edu_1_period'),
        'home_journey_edu_1_desc': get_general_setting('home_journey_edu_1_desc'),
        'home_journey_edu_2_school': get_general_setting('home_journey_edu_2_school'),
        'home_journey_edu_2_period': get_general_setting('home_journey_edu_2_period'),
        'home_journey_edu_2_desc': get_general_setting('home_journey_edu_2_desc'),
        'skills': Skill.objects.all().order_by('order'),
        'experiences': Experience.objects.all().order_by('-start_date'),
        'educations': Education.objects.all().order_by('-start_date'),
        'projects': Project.objects.exclude(status=Project.Status.DRAFT).select_related('category').prefetch_related('hero_links').order_by('order', 'created_at'),
        'journey_default_tab': site_preference.default_journey_tab,
    })
    return render(request, 'index.html', context=context)


def redirect_urls(request, slug):
    doc = get_object_or_404(Document, slug=slug)
    return redirect(doc.file.url)
