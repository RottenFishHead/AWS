from django import forms
from .models import PokerSession, SessionNotes
from datetime import date
from .fields import STAKES_CHOICES

class SessionNotesForm(forms.ModelForm):
    class Meta:
        model = SessionNotes
        fields = ['tags', 'notes', 'takeaway']  # The fields you want to capture
        widgets = {
            'tag': forms.Select()
        }
        
    def __init__(self, *args, **kwargs):
        super(SessionNotesForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


            
class PokerSessionForm(forms.ModelForm):
    date = forms.DateField(widget = forms.SelectDateWidget(),initial=date.today)
    class Meta:
        model = PokerSession
        fields = ['player', 'casino', 'stakes', 'date', 'hours', 'buy_in', 'cash_out']
        
class DateForm(forms.Form):
    start = forms.DateField(help_text="Must always include a date range",
        widget=forms.DateInput(attrs={'type': 'date', 'style':'width:150px;'}))
    end = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'style':'width:150px;'}))
    stakes = forms.TypedChoiceField(choices=STAKES_CHOICES)
    