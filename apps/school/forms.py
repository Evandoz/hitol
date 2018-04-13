# -*- coding: utf-8 -*-
import re

from django import forms

from operation.models import UserAsk

'''
class UserAskForm(forms.form):
	name = forms.CharField(required=True, min_length=2, max_length=20)
	phone = forms.CharField(required=True, min_length=11, max_length=20)
	course_name = forms.CharField(required=True, min_length=5, max_length=50)
'''


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        regex_mobile = '1[3458]\\d{9}'
        p = re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号码非法', code='mobile_invalid')
