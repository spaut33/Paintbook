from django.db import models


# Create your models here.
class Manufacturer(models.Model):
    def __str__(self):
        return '{}'.format(self.name)

    name = models.CharField('Manufacturer\'s name', max_length=255)


class Series(models.Model):
    def __str__(self):
        return '{}'.format(self.name)

    name = models.CharField('Series name', max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)


class Paint(models.Model):
    def __str__(self):
        return '#{} {}'.format(self.id, self.name)

    class PaintTypes(models.TextChoices):
        PAINT = 'Paint'
        WASH = 'Wash'
        FILTER = 'Filter'
        PASTE = 'Texture paste'

    class Bases(models.TextChoices):
        ACRYLIC = 'Acrylic'
        ENAMEL = 'Enamel'
        OIL = 'Oil'

    class Opacity(models.TextChoices):
        OPAQUE = 'Opaque'
        SEMI = 'Semi-transparent'
        TRANSPARENT = 'Transparent'

    class Gloss(models.TextChoices):
        MATT = 'Matt'
        SEMI = 'Semi-gloss'
        GLOSS = 'Gloss'

    name = models.CharField('Name', max_length=255)
    paint_type = models.CharField(
        'Paint type',
        max_length=50,
        choices=PaintTypes.choices,
        default=PaintTypes.PAINT,
    )
    article = models.CharField('art. number', max_length=100, default='')
    manufacturer = models.ForeignKey(
        Manufacturer, verbose_name='Manufacturer\'s name', on_delete=models.CASCADE, null=False, default=1
    )
    series = models.ForeignKey(
        Series, verbose_name='Series name', on_delete=models.SET_NULL, null=True, default=1
    )
    description = models.CharField('Description', max_length=255, default='')
    color = models.CharField('#FFFFFF format color', max_length=6, default='')
    base = models.CharField(
        'Base type', max_length=50, choices=Bases.choices, default=Bases.ACRYLIC
    )
    opacity = models.CharField(
        'Opacity', max_length=50, choices=Opacity.choices, default=Opacity.OPAQUE
    )
    gloss = models.CharField(
        'Glossiness', max_length=50, choices=Gloss.choices, default=Gloss.MATT
    )
    metallic = models.BooleanField('Metallic', default=False)
    quantity = models.PositiveSmallIntegerField('Total quantity', default=1)
    time_added = models.DateTimeField('Date added', auto_now=True)
