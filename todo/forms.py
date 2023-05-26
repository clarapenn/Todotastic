from django import forms
from todo.models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        # in Django, a Meta class is used to define configurable options
        # that the class needs - eg which Model we are making a Form for, in this case
        model = Todo
        exclude = ("id",)  # ie, we don't want to be able to edit the id of the Todo

    def __init__(self, *args, **kwargs):
        # First, call the real constructor from the base class, so that
        # we initialise a form object. so that we can add extra attributes
        # to the fields it will render.
        super().__init__(*args, **kwargs)

        # self.fields is a dictionary of pairs of fieldname (string) + Python field (an object)
        # {
        #   'name': <django.forms.fieldsField instance at 0x0161612721712>,
        #   'age': <django.forms.fieldsField instance at 0x01616127223234>
        # }
        # And because it's a dictionary, we can loop through its keys, its items or just its values

        # # So we loop through and add a css-class attribute to each field object's attrs dictionary:
        # for field in self.fields.values():
        #     field.widget.attrs.update({"class": "form-control"})

        #     # we use 'update' so that we only add to amy existing 'class' attributes
        #     # because if we did
        #     #       field.widget.attrs['class'] = 'form-control'
        #     # that would replace it wholesale

        # BUT we don't do that because it's not nearly nuanced enough and breaks things like
        # checkboxes

        # Let's specify manually which class to add to which field:

        self.fields["task"].widget.attrs.update({"class": "form-control"})
        self.fields["completed"].widget.attrs.update({"class": "form-check-input"})

