from django import forms
from django.forms.forms import BoundField
from django.forms import widgets
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


class LocalBaseForm():
    def __init__(self, *args, **kwargs):
        self.error_css_class = 'invalid'
        self.required_css_class = 'required'
        super(LocalForm, self).__init__(*args, **kwargs)

    def _html_output_as_dl(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        "Helper function for outputting HTML. Used by as_table(), as_ul(), as_p()."
        top_errors = self.non_field_errors() # Errors that should be displayed above all fields.
        mark_as_required_field = _('mark as required field')
        output, hidden_fields = [], []

        for name, field in self.fields.items():
            html_class_attr = ''
            bf = BoundField(self, field, name)
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors]) # Escape and cache in local variable.
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend([u'(Hidden field %s) %s' % (name, force_unicode(e)) for e in bf_errors])
                hidden_fields.append(unicode(bf))
            else:
                # Create a 'class="..."' atribute if the row should have any
                # CSS classes applied.
                widget_type = type(field.widget)
                widget_base_type = widget_type.__bases__[0]
                extra_classes = None
                if widget_base_type == widgets.Input:
                    if widget_type == widgets.FileInput:
                        extra_classes = 'input_file'
                    else:
                        extra_classes = 'input_text'
                elif widget_base_type == widgets.Widget:
                    if widget_type == widgets.Select:
                        extra_classes = 'select'
                    elif widget_type == widgets.Textarea:
                        extra_classes = 'textarea'
                    elif widget_type == widgets.CheckboxInput:
                        extra_classes = 'input_checkbox'
                elif widget_base_type == widgets.Select:
                    if widget_type == widgets.RadioSelect:
                        extra_classes = 'input_radio'
                css_classes = bf.css_classes(extra_classes)
                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes

                if errors_on_separate_row and bf_errors:
                    output.append(error_row % force_unicode(bf_errors))

                if bf.label:
                    label = conditional_escape(force_unicode(bf.label))
                    if bf.field.required and (widget_base_type == widgets.Input\
                        or widget_type == widgets.Textarea):
                        label += mark_as_required_field
                    # Only add the suffix if the label does not end in
                    # punctuation.
                    if self.label_suffix:
                        if label[-1] not in ':?.!':
                            label += self.label_suffix
                    label = bf.label_tag(label) or ''
                else:
                    label = ''

                if field.help_text:
                    help_text = help_text_html % force_unicode(field.help_text)
                else:
                    help_text = u''

                output.append(normal_row % {
                    'errors': force_unicode(bf_errors),
                    'label': force_unicode(label),
                    'field': unicode(bf),
                    'help_text': help_text,
                    'html_class_attr': html_class_attr
                })

        if top_errors:
            output.insert(0, error_row % force_unicode(top_errors))

        if hidden_fields: # Insert any hidden fields in the last row.
            str_hidden = u''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = (normal_row % {'errors': '', 'label': '',
                                              'field': '', 'help_text':'',
                                              'html_class_attr': html_class_attr})
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        return mark_safe(u'\n'.join(output))

    def as_dl(self):
        "Returns this form rendered as HTML <tr>s -- excluding the <table></table>."
        return self._html_output_as_dl(
            normal_row = u"""<dl%(html_class_attr)s><dt class="label">%(label)s</dt><dd class="field">%(field)s%(help_text)s%(errors)s</dd></dl>""",
            error_row = u'<div class="form__errors">%s</div>',
            row_ender = u'',
            help_text_html = u'<br /><span class="note">%s</span>',
            errors_on_separate_row = False)

class LocalForm(forms.Form, LocalBaseForm):
    pass

class LocalModelForm(forms.ModelForm, LocalBaseForm):
    pass
