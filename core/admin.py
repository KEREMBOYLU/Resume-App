from django.contrib import admin
from django import forms
from datetime import date
from core.models import *
from portfolio_website.widgets import AdminImageEditorWidget


# Register your models here.

@admin.register(GeneralSetting)
class GeneralSettingAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'parameter', 'updated_date', 'created_date']
    search_fields = ['name', 'description', 'parameter','text_parameter',]
    list_editable = ['description', 'parameter',]

    class Meta:
        model = GeneralSetting


class ImageSettingAdminForm(forms.ModelForm):
    class Meta:
        model = ImageSetting
        fields = '__all__'
        widgets = {
            'file': AdminImageEditorWidget(),
        }


@admin.register(ImageSetting)
class ImageSettingAdmin(admin.ModelAdmin):
    form = ImageSettingAdminForm
    list_display = ['id', 'name', 'description', 'file', 'updated_date', 'created_date']
    search_fields = ['name', 'description', 'file']
    list_editable = ['description', 'file']

    class Meta:
        model = ImageSetting


@admin.register(SitePreference)
class SitePreferenceAdmin(admin.ModelAdmin):
    list_display = ['id', 'default_journey_tab', 'updated_date', 'created_date']

    def has_add_permission(self, request):
        return not SitePreference.objects.exists()

    class Meta:
        model = SitePreference


@admin.register(Skill)
class SkillSettingAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'name', 'category', 'updated_date', 'created_date']
    search_fields = ['name', 'category']
    list_editable = ['order', 'name', 'category']

    class Meta:
        model = Skill


def _month_choices():
    return [
        ('', 'Month'),
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]


def _year_choices():
    current = date.today().year
    years = [('', 'Year')]
    years.extend((str(y), str(y)) for y in range(current + 5, 1969, -1))
    return years


class ExperienceAdminForm(forms.ModelForm):
    start_date = forms.DateField(required=False, widget=forms.HiddenInput())
    end_date = forms.DateField(required=False, widget=forms.HiddenInput())
    start_month = forms.ChoiceField(choices=_month_choices(), required=True, label='Start month')
    start_year = forms.ChoiceField(choices=_year_choices(), required=True, label='Start year')
    end_month = forms.ChoiceField(choices=_month_choices(), required=False, label='End month')
    end_year = forms.ChoiceField(choices=_year_choices(), required=False, label='End year')

    class Meta:
        model = Experience
        fields = '__all__'
        widgets = {
            'start_date': forms.HiddenInput(),
            'end_date': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.start_date:
                self.initial['start_month'] = str(self.instance.start_date.month)
                self.initial['start_year'] = str(self.instance.start_date.year)
            if self.instance.end_date:
                self.initial['end_month'] = str(self.instance.end_date.month)
                self.initial['end_year'] = str(self.instance.end_date.year)

    def clean(self):
        cleaned = super().clean()

        try:
            start_month = int(cleaned.get('start_month'))
            start_year = int(cleaned.get('start_year'))
            cleaned['start_date'] = date(start_year, start_month, 1)
        except (TypeError, ValueError):
            raise forms.ValidationError('Start date month and year are required.')

        end_month_raw = cleaned.get('end_month')
        end_year_raw = cleaned.get('end_year')
        if end_month_raw or end_year_raw:
            if not end_month_raw or not end_year_raw:
                raise forms.ValidationError('Please select both end month and end year.')
            try:
                end_month = int(end_month_raw)
                end_year = int(end_year_raw)
                cleaned['end_date'] = date(end_year, end_month, 1)
            except (TypeError, ValueError):
                raise forms.ValidationError('End date is invalid.')
        else:
            cleaned['end_date'] = None

        if cleaned.get('end_date') and cleaned['end_date'] < cleaned['start_date']:
            raise forms.ValidationError('End date cannot be before start date.')

        return cleaned


@admin.register(Experience)
class ExperienceSettingAdmin(admin.ModelAdmin):
    form = ExperienceAdminForm
    list_display = ['id', 'company_name', 'job_title', 'job_location', 'start_date', 'end_date', 'updated_date',
                    'created_date']
    search_fields = ['company_name', 'job_title', 'job_location']
    list_editable = ['company_name', 'job_title', 'job_location']

    class Meta:
        model = Experience


class EducationAdminForm(forms.ModelForm):
    start_date = forms.DateField(required=False, widget=forms.HiddenInput())
    end_date = forms.DateField(required=False, widget=forms.HiddenInput())
    start_month = forms.ChoiceField(choices=_month_choices(), required=True, label='Start month')
    start_year = forms.ChoiceField(choices=_year_choices(), required=True, label='Start year')
    end_month = forms.ChoiceField(choices=_month_choices(), required=False, label='End month')
    end_year = forms.ChoiceField(choices=_year_choices(), required=False, label='End year')

    class Meta:
        model = Education
        fields = '__all__'
        widgets = {
            'start_date': forms.HiddenInput(),
            'end_date': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.start_date:
                self.initial['start_month'] = str(self.instance.start_date.month)
                self.initial['start_year'] = str(self.instance.start_date.year)
            if self.instance.end_date:
                self.initial['end_month'] = str(self.instance.end_date.month)
                self.initial['end_year'] = str(self.instance.end_date.year)

    def clean(self):
        cleaned = super().clean()

        try:
            start_month = int(cleaned.get('start_month'))
            start_year = int(cleaned.get('start_year'))
            cleaned['start_date'] = date(start_year, start_month, 1)
        except (TypeError, ValueError):
            raise forms.ValidationError('Start date month and year are required.')

        end_month_raw = cleaned.get('end_month')
        end_year_raw = cleaned.get('end_year')
        if end_month_raw or end_year_raw:
            if not end_month_raw or not end_year_raw:
                raise forms.ValidationError('Please select both end month and end year.')
            try:
                end_month = int(end_month_raw)
                end_year = int(end_year_raw)
                cleaned['end_date'] = date(end_year, end_month, 1)
            except (TypeError, ValueError):
                raise forms.ValidationError('End date is invalid.')
        else:
            cleaned['end_date'] = None

        if cleaned.get('end_date') and cleaned['end_date'] < cleaned['start_date']:
            raise forms.ValidationError('End date cannot be before start date.')

        return cleaned


@admin.register(Education)
class EducationSettingAdmin(admin.ModelAdmin):
    form = EducationAdminForm
    list_display = ['id', 'school_name', 'major', 'department','school_location', 'start_date', 'end_date', 'updated_date',
                    'created_date']
    search_fields = ['school_name', 'major', 'department','school_location',]
    list_editable = ['school_name', 'major', 'department','school_location']

    class Meta:
        model = Education


@admin.register(SocialMedia)
class SocialMediaSettingAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'name', 'link', 'icon', 'updated_date', 'created_date']
    search_fields = ['name', 'link', 'icon']
    list_editable = ['order', 'name', 'link', 'icon']

    class Meta:
        model = SocialMedia


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'slug', 'button_text', 'file', 'updated_date', 'created_date']
    search_fields = ['slug', 'button_text', ]
    list_editable = ['order', 'slug', 'button_text', 'file']

    class Meta:
        model = Document
