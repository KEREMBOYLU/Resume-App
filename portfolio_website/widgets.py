from django.forms.widgets import ClearableFileInput
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class AdminImageEditorWidget(ClearableFileInput):
    template_name = 'admin/widgets/admin_image_editor.html'

    class Media:
        css = {
            'all': (
                'https://cdn.jsdelivr.net/npm/cropperjs@1.6.2/dist/cropper.min.css',
                'admin/css/admin_image_editor.css',
            )
        }
        js = (
            'https://cdn.jsdelivr.net/npm/cropperjs@1.6.2/dist/cropper.min.js',
            'admin/js/admin_image_editor.js',
        )

    def __init__(self, attrs=None):
        attrs = attrs.copy() if attrs else {}
        attrs['accept'] = attrs.get('accept', 'image/*')
        attrs['class'] = f"{attrs.get('class', '')} admin-image-editor__input".strip()
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        widget = context['widget']
        widget['preview_url'] = value.url if value and hasattr(value, 'url') else ''
        return context

    def _render(self, template_name, context, renderer=None):
        return mark_safe(render_to_string(template_name, context))


CroppableImageWidget = AdminImageEditorWidget
