from django.db import models
from django.urls import reverse

from portfolio_website.custom_storage import MediaStorage


class ProjectCategory(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    icon = models.CharField(max_length=80, blank=True)

    class Meta:
        verbose_name = 'Project Category'
        verbose_name_plural = 'Project Categories'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Project(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'

    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    summary = models.TextField()
    cover_image = models.ImageField(storage=MediaStorage(), upload_to='projects/covers/')
    category = models.ForeignKey(
        ProjectCategory,
        related_name='projects',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    tech_stack = models.CharField(max_length=300, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order', 'created_at')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})

    @property
    def tech_stack_items(self):
        return [item.strip() for item in self.tech_stack.split(',') if item.strip()]


class ProjectLink(models.Model):
    project = models.ForeignKey(Project, related_name='hero_links', on_delete=models.CASCADE)
    label = models.CharField(max_length=80)
    url = models.URLField()
    icon = models.CharField(max_length=80, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('order', 'id')

    def __str__(self):
        return f'{self.project.title}: {self.label}'


class ProjectImage(models.Model):
    class ImageType(models.TextChoices):
        CAROUSEL = 'carousel', 'Carousel'
        GALLERY = 'gallery', 'Gallery'

    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(storage=MediaStorage(), upload_to='projects/images/')
    image_type = models.CharField(max_length=20, choices=ImageType.choices, default=ImageType.GALLERY)
    alt_text = models.CharField(max_length=180, blank=True)
    caption = models.CharField(max_length=220, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('order', 'id')

    def __str__(self):
        return f'{self.project.title}: {self.get_image_type_display()} image'


class ProjectSection(models.Model):
    class SectionType(models.TextChoices):
        GALLERY = 'gallery', 'Gallery'
        FEATURE_LIST = 'feature_list', 'Feature List'
        TIMELINE = 'timeline', 'Timeline'
        CUSTOM_HTML = 'custom_html', 'Custom HTML'

    project = models.ForeignKey(Project, related_name='sections', on_delete=models.CASCADE)
    section_type = models.CharField(max_length=30, choices=SectionType.choices)
    title = models.CharField(max_length=160, blank=True)
    content = models.TextField(blank=True)
    data = models.JSONField(default=dict, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('order', 'id')

    def __str__(self):
        label = self.title or self.get_section_type_display()
        return f'{self.project.title}: {label}'

    @property
    def feature_items(self):
        if isinstance(self.data, list):
            return self.data
        if isinstance(self.data, dict):
            return self.data.get('features', [])
        return []

    @property
    def timeline_items(self):
        if isinstance(self.data, list):
            return self.data
        if isinstance(self.data, dict):
            return self.data.get('items') or self.data.get('timeline', [])
        return []
