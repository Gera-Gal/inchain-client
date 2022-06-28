from django.db import models
from django.core.validators import MinValueValidator

class Course(models.Model):
    title = models.CharField(max_length=255, unique=True, default='')
    content = models.TextField()
    slug = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

class MediaFile(models.Model):
    class FormatType(models.TextChoices):
        LEFT_INLINE = 'l-in', 'Left Inline'
        RIGHT_INLINE = 'r-in', 'Right Inline'
        CENTER_FULL = 'c-full', 'Center Full Screen'

    caption = models.CharField(max_length=255)
    media_file = models.CharField(max_length=255)
    format = models.CharField(max_length=6, choices=FormatType.choices)
    course = models.ForeignKey(Course, on_delete=models.RESTRICT)
    argument_number = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0}>>{1}'.format(self.format, self.caption)

    def html_format(self):
        return '''
        <div class="course-img-{0}">
            <figure>
                <img src="{1}" alt="">
            </figure>
            <p class="text-muted"><small>{2}</small></p>
        </div>
        '''.format(self.format, self.media_file, self.caption)