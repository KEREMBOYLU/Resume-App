from django.test import TestCase
from django.urls import reverse

from .models import Project, ProjectCategory, ProjectImage, ProjectSection


class ProjectPublicViewTests(TestCase):
    def create_project(self, title, slug, status=Project.Status.COMPLETED, order=0):
        category = ProjectCategory.objects.create(name='SaaS', slug='saas')
        return Project.objects.create(
            title=title,
            slug=slug,
            summary='Short project summary.',
            cover_image=f'projects/covers/{slug}.gif',
            category=category,
            status=status,
            order=order,
        )

    def test_project_list_hides_drafts(self):
        visible = self.create_project('Visible Project', 'visible-project')
        Project.objects.create(
            title='Draft Project',
            slug='draft-project',
            summary='Draft summary.',
            cover_image='projects/covers/draft.gif',
            status=Project.Status.DRAFT,
        )

        response = self.client.get(reverse('projects'))

        self.assertContains(response, visible.title)
        self.assertNotContains(response, 'Draft Project')

    def test_project_detail_404s_for_draft_project(self):
        draft = self.create_project('Draft Project', 'draft-project', status=Project.Status.DRAFT)

        response = self.client.get(reverse('project_detail', kwargs={'slug': draft.slug}))

        self.assertEqual(response.status_code, 404)

    def test_project_detail_renders_active_sections_and_gallery_images(self):
        project = self.create_project('Visible Project', 'visible-project')
        ProjectSection.objects.create(
            project=project,
            section_type=ProjectSection.SectionType.FEATURE_LIST,
            title='Features',
            data={'features': [{'title': 'Admin managed'}]},
            is_active=True,
        )
        ProjectSection.objects.create(
            project=project,
            section_type=ProjectSection.SectionType.CUSTOM_HTML,
            title='Hidden',
            content='<p>Hidden content</p>',
            is_active=False,
        )
        ProjectImage.objects.create(
            project=project,
            image='projects/images/gallery.gif',
            image_type=ProjectImage.ImageType.GALLERY,
            alt_text='Gallery alt',
            is_active=True,
        )
        ProjectImage.objects.create(
            project=project,
            image='projects/images/carousel.gif',
            image_type=ProjectImage.ImageType.CAROUSEL,
            alt_text='Carousel alt',
            is_active=True,
        )

        response = self.client.get(reverse('project_detail', kwargs={'slug': project.slug}))

        self.assertContains(response, 'Features')
        self.assertContains(response, 'Admin managed')
        self.assertContains(response, 'Gallery alt')
        self.assertNotContains(response, 'Hidden content')
        self.assertNotContains(response, 'Carousel alt')
