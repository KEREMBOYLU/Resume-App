from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render

from core.views import layout

from .models import Project, ProjectImage, ProjectSection


def public_projects():
    return Project.objects.exclude(status=Project.Status.DRAFT)


def project_list(request):
    projects = (
        public_projects()
        .select_related('category')
        .order_by('order', 'created_at')
    )
    context = layout(request)
    context['projects'] = projects
    context['page_title'] = context['gs'].get('projects_page_title') or 'Projects'
    return render(request, 'projects/project_list.html', context)


def project_detail(request, slug):
    active_sections = ProjectSection.objects.filter(is_active=True).order_by('order', 'id')
    project = get_object_or_404(
        public_projects()
        .select_related('category')
        .prefetch_related(
            'hero_links',
            Prefetch('sections', queryset=active_sections),
        ),
        slug=slug,
    )
    project_sections = list(project.sections.all())
    overview_section = next(
        (
            section for section in project_sections
            if section.section_type == ProjectSection.SectionType.CUSTOM_HTML
            and section.title.strip().lower() == 'project overview'
        ),
        None,
    )
    content_sections = [
        section for section in project_sections
        if section != overview_section
    ]
    gallery_images = project.images.filter(
        image_type=ProjectImage.ImageType.GALLERY,
        is_active=True,
    ).order_by('order', 'id')
    has_gallery_section = any(
        section.section_type == ProjectSection.SectionType.GALLERY
        for section in project_sections
    )

    context = layout(request)
    context.update({
        'project': project,
        'overview_section': overview_section,
        'content_sections': content_sections,
        'gallery_images': gallery_images,
        'has_gallery_section': has_gallery_section,
    })
    return render(request, 'projects/project_detail.html', context)
