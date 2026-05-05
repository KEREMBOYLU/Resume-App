from django.contrib import admin
from django import forms
from django.utils.html import format_html

from portfolio_website.widgets import AdminImageEditorWidget

from .models import Project, ProjectCategory, ProjectImage, ProjectLink, ProjectSection


class ImagePreviewMixin:
    def image_preview(self, obj):
        if not obj or not obj.image:
            return '-'
        return format_html(
            '<img src="{}" style="width: 80px; height: 50px; object-fit: cover; border-radius: 6px;" />',
            obj.image.url,
        )

    image_preview.short_description = 'Preview'


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('name',)


class ProjectLinkInline(admin.TabularInline):
    model = ProjectLink
    extra = 1
    fields = ('label', 'url', 'icon', 'is_primary', 'order')
    ordering = ('order', 'id')


class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'cover_image': AdminImageEditorWidget(),
        }


class ProjectImageAdminForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = '__all__'
        widgets = {
            'image': AdminImageEditorWidget(),
        }


class ProjectImageInline(ImagePreviewMixin, admin.TabularInline):
    model = ProjectImage
    form = ProjectImageAdminForm
    extra = 1
    fields = ('image_preview', 'image', 'image_type', 'alt_text', 'caption', 'order', 'is_active')
    readonly_fields = ('image_preview',)
    ordering = ('order', 'id')


class ProjectSectionInline(admin.StackedInline):
    model = ProjectSection
    extra = 1
    fields = ('section_type', 'title', 'order', 'is_active', 'content', 'data')
    ordering = ('order', 'id')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    inlines = (ProjectLinkInline, ProjectImageInline, ProjectSectionInline)
    list_display = ('title', 'category', 'status', 'is_featured', 'order', 'created_at')
    list_filter = ('category', 'status', 'is_featured')
    search_fields = ('title', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order', '-created_at')
    list_editable = ('status', 'is_featured', 'order')

    class Media:
        js = ('admin/js/project_json_import.js',)


@admin.register(ProjectLink)
class ProjectLinkAdmin(admin.ModelAdmin):
    list_display = ('label', 'project', 'url', 'icon', 'is_primary', 'order')
    list_filter = ('is_primary', 'project')
    search_fields = ('label', 'url', 'project__title')
    ordering = ('project', 'order')


@admin.register(ProjectImage)
class ProjectImageAdmin(ImagePreviewMixin, admin.ModelAdmin):
    form = ProjectImageAdminForm
    list_display = ('project', 'image_preview', 'image_type', 'order', 'is_active')
    list_filter = ('project', 'image_type', 'is_active')
    search_fields = ('project__title', 'alt_text', 'caption')
    ordering = ('project', 'order')
    readonly_fields = ('image_preview',)


@admin.register(ProjectSection)
class ProjectSectionAdmin(admin.ModelAdmin):
    list_display = ('project', 'section_type', 'title', 'order', 'is_active')
    list_filter = ('project', 'section_type', 'is_active')
    search_fields = ('project__title', 'title', 'content')
    ordering = ('project', 'order')
