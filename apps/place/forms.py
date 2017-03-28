#-*- coding: utf-8 -*-
from django import forms
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory

from elrte.widgets import ElrteTextareaWidget


from place.models import Place, PlaceAddress, PlaceAddressWorkTime,\
                            PlaceGallery, PlaceCategory, FoursquarePhoto
from common.fields import EmailsListField
from tagging.models import Tag


class SelectMutliple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        choices.sort()
        return super(SelectMutliple, self).render(name, value, attrs, choices)

class ChangeCategoryForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    categorys = forms.ModelMultipleChoiceField(
       queryset=PlaceCategory.objects.all().order_by('name', 'main_tag__name'),
       label=u'Выберите категории',
       widget=forms.CheckboxSelectMultiple
    )


class ChangeTaggingForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    categorys = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by('name'),
        label=u'Выберите категории',
        widget=forms.CheckboxSelectMultiple
    )


class PlaceForm(forms.ModelForm):

    description = forms.CharField(label=u"Описание",
                            widget=ElrteTextareaWidget(),
                            required=False,)
    email = EmailsListField(label=u"Электронная почта",
                            required=False,)
    date_mark_as_new = forms.DateTimeField(label='date of mark as new',
                            widget=forms.HiddenInput(), required=False)

    class Meta:
        exclude = ['num_comments', 'hits', 'urlhits']
        model = Place


class PlaceAddressForm(forms.ModelForm):

    class Meta:
        fields = (
            'is_main_office',
            'address', 'geopoint', 'phone',
            'district', 'email', 'id', 'fsid',
        )
        model = PlaceAddress

    def has_instance(self):
        if hasattr(self, 'instance') and self.instance.id:
            return True
        return False


class PlaceAddressWorkTimeFormSet(BaseInlineFormSet):

    class Meta:
        pass


class PlaceAddressWorkTimeForm(forms.ModelForm):

    all_day = forms.BooleanField(label=u"Ежедневно",
                                required=False,)
    day_off = forms.BooleanField(label=u"Выходные дни",
                                required=False)

    class Meta:
        model = PlaceAddressWorkTime

        widgets = {
            "address": forms.HiddenInput,
        }


class PlaceGalerryForm(forms.ModelForm):

    title = forms.CharField(
                required=False,
                label=u"Описание",
                widget=forms.Textarea(
                        attrs={
                            "cols": "30",
                            "rows": "5",
                        }))

    crop_x = forms.FloatField(required=False,
            widget=forms.HiddenInput(attrs={'class': 'coordinate'}))
    crop_y = forms.FloatField(required=False,
            widget=forms.HiddenInput(attrs={'class': 'coordinate'}))
    crop_x2 = forms.FloatField(required=False,
            widget=forms.HiddenInput(attrs={'class': 'coordinate'}))
    crop_y2 = forms.FloatField(required=False,
            widget=forms.HiddenInput(attrs={'class': 'coordinate'}))

    class Meta:
        model = PlaceGallery

        widgets = {
            "image": forms.FileInput,
            "order": forms.HiddenInput,
        }

    def has_image(self):
        if self.has_instance():
            return bool(self.instance.image)
        return False

    def has_instance(self):
        return hasattr(self, 'instance')\
                and self.instance.id\
                and bool(self.instance.image)

    def save(self, *args, **kwargs):
        self.cleaned_data['image'] = None
        return super(PlaceGalerryForm, self).save(*args, **kwargs)


class PlaceAddressFormSet(BaseInlineFormSet):

    class Meta:
        pass


# class FoursquarePhotoForm(forms.ModelForm):
#     class Meta:
#         model = FoursquarePhoto

#     def thumb_url(self):
#         if self.has_instance():
#             return self.instance.thumb_url()
#         return '';


class PlaceGalerryFormSet(BaseInlineFormSet):

    def __iter__(self):
        forms = self.forms
        forms.sort(key=lambda x: x.instance.order if x.instance.id else 12)
        return iter(forms)

    class Meta:
        pass


WorkTimeSet = inlineformset_factory(PlaceAddress,
                            PlaceAddressWorkTime,
                            can_delete=True,
                            extra=0)

AddressSet = inlineformset_factory(Place, PlaceAddress,
                            formset=PlaceAddressFormSet,
                            form=PlaceAddressForm,
                            can_delete=True,
                            extra=0)

GallerySet = inlineformset_factory(Place, PlaceGallery,
                            formset=PlaceGalerryFormSet,
                            form=PlaceGalerryForm,
                            can_delete=True,)

FoursquarePhotoSet = inlineformset_factory(Place, FoursquarePhoto,
                            can_delete=False,
                            fields = ('is_published',),
                            extra=0)
