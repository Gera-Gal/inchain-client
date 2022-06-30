from django import forms
from .models import MediaFile, Course

format_choices = [
    ('L-IN', 'Left Inline'),
    ('R-IN', 'Right Inline'),
    ('C-FULL', 'Center Full Screen')
]

class CreateCourseForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    slug = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    caption = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    media_file = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    format = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'},choices=format_choices))
    argument_number = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        slug_exists = Course.objects.filter(slug=slug).exists()
        if slug_exists:
            raise forms.ValidationError(
                "El slug del curso no está disponible"
            )
        return slug

    def clean(self):
        data = self.cleaned_data
        title = data.get("title")
        content = data.get("content")
        caption = data.get("caption")
        media_file = data.get("media_file")
        format = data.get("format")
        argument_number = data.get("argument_number")
        return data

    def save(self):
        media_keys = ['caption', 'media_file', 'format', 'argument_number']
        course_keys = ['title', 'content', 'slug']
        course_data = self.cleaned_data.copy()
        media_data = self.cleaned_data.copy()
        for key in media_keys:
            course_data.pop(key)
        course = Course.objects.create(**course_data)
        for key in course_keys:
            media_data.pop(key)
        #print('course: {}'.format(course), 'media: {}'.format(media_data))
        media_data['course_id'] = course.id
        media = MediaFile.objects.create(**media_data)
        #print(course, media)