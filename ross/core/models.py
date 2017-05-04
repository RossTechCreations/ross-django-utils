from __future__ import unicode_literals

from django.db import models, IntegrityError
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class Timestamped(models.Model):
    """
    Adds created and updated fields to a model.
    """
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        abstract = True


class Slugged(models.Model):
    """
    Adds slug field and a slug-generating function on save() to a model.
    
    Configuration:
    
    value_field_name
        The field of the model that a slug will be generated from.
        Note: You will have to manually add this field to your model
        default: 'title'
        
    slug_field_name
        The field of the model the slug will be stored in. 
        default: 'slug'
        
    max_iterations
        How many iterations the save() method will try before it gives up. 
        default: 1000
        
    slug_separator
        The separator between slug words. Must be url-safe. 
        default: '-'
    """
    slug = models.CharField(
        _('URL'), help_text=_('URL of the page. Leave blank to be auto-generated'),
        max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            pk_field_name = self._meta.pk.name
            value_field_name = getattr(self, 'value_field_name', 'title')
            slug_field_name = getattr(self, 'slug_field_name', 'slug')
            max_interations = getattr(self, 'slug_max_iterations', 1000)
            slug_separator = getattr(self, 'slug_separator', '-')

            # setup
            slug_field = self._meta.get_field(slug_field_name)
            slug_len = slug_field.max_length
            queryset = self.__class__.objects.all()

            # exclude current record pk (if it is defined) it from the slug search
            current_pk = getattr(self, pk_field_name)
            if current_pk:
                queryset = queryset.exclude(**{pk_field_name: current_pk})

            # Checks if the field defined in value_field_name exist
            value_field = getattr(self, value_field_name, None)
            if value_field:
                slug = slugify(getattr(self, value_field_name))
                if slug_len:
                    slug = slug[:slug_len]
                original_slug = slug
            else:
                raise IntegrityError('The source field %s doesn\'t exist!' % value_field_name)

            # loop until a unique slug is found, or max_iterations is reached
            counter = 2
            while queryset.filter(
                    **{slug_field_name: slug}
            ).count() > 0 and counter < max_interations:
                slug = original_slug
                suffix = '%s%s' % (slug_separator, counter)
                if slug_len and len(slug) + len(suffix) > slug_len:
                    slug = slug[:slug_len - len(suffix)]
                slug = '%s%s' % (slug, suffix)
                counter += 1

            if counter == max_interations:
                raise IntegrityError('Unable to locate unique slug')

            setattr(self, slug_field.attname, slug)

        super(Slugged, self).save(*args, **kwargs)

    class Meta:
        abstract = True
