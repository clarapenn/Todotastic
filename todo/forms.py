from django import forms
from todo.models import Todo
import datetime


class TodoForm(forms.ModelForm):
    class Meta:
        # in Django, a Meta class is used to define configurable options
        # that the class needs - eg which Model we are making a Form for, in this case
        model = Todo
        fields = (
            "task",
            "date_due",
            "priority",
        )
        # it's better to be explicit about what we want, rather than just exclude what we don't want
        # because excluding a fixed list of fields means new fields on the model would appear in the
        # form unless they are added to an exclude clause

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
        self.fields["priority"].widget.attrs.update({"class": "form-select"})
        # self.fields["date_due"].widget = forms.SelectDateWidget()


class CompletionForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = (
            "id",
        )  # TODO: use this ID to verify the Todo we're updating is definitely the right one.

    # Saving logic has been moved to the model

    # def save(self, *args, **kwargs):

    #     # Use the modelform's save() method to get us an updated _but unsaved_ todo instance
    #     # (the commit=False is what stops the actual save to the database)
    #     updated_todo = super().save(*args, commit=False, **kwargs)

    #     # updated_todo can be edited/changed as we need, so let's force it to be completed
    #     # and use today as the date of completion
    #     updated_todo.completed = True
    #     updated_todo.date_completed = datetime.date.today()

    #     # And now we can save it to the database, including the values we slotted in for
    #     # completed and date_completed
    #     updated_todo.save()
    #     return updated_todo


class AddForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ("task",)

    def __init__(self, *args, **kwargs):
        # First, call the real constructor from the base class, so that
        # we initialise a form object. so that we can add extra attributes
        # to the fields it will render.
        super().__init__(*args, **kwargs)

        self.fields["task"].widget.attrs.update({"class": "form-control"})


class DeletionForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ("id",)
