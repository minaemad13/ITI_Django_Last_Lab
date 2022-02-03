from django import forms

from student.models import info


class InsertStudent(forms.Form):
    fullname = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)
    Email = forms.EmailField(max_length=240)


class InsertStudent1(forms.ModelForm):
    class Meta:
        model = info
        fields = ['fullname', 'password','Email']
