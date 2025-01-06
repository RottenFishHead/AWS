from django.shortcuts import render, get_object_or_404, redirect
from .models import PokerSession, SessionNotes
from poker.forms import PokerSessionForm, DateForm, SessionNotesForm
from django.utils import timezone
from django.db.models import Sum, ExpressionWrapper, F, DurationField, Q
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from plotly.offline import plot
from plotly import graph_objs as go
import plotly.express as px
import pandas as pd
from calendar import month_name
from datetime import timedelta
    
@login_required
def index(request):
    stakes_filter = request.GET.get('stakes')
    sessions =  PokerSession.objects.filter(player=request.user)
    current_month = timezone.now().month
    current_year = timezone.now().year
    overall_total = sum(session.win_loss for session in sessions)
    overall_hours = sum(session.hours for session in sessions)
    overall_hourly_rate = overall_total / overall_hours if overall_hours > 0 else 0
    
    if stakes_filter:
            sessions = sessions.filter(stakes=stakes_filter)

    sessions_by_month = sessions.annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        total_profit=Sum('cash_out') - Sum('buy_in'),
        total_hours=Sum('hours')
    ).order_by('-month')

    for session in sessions_by_month:
        if session['total_hours']:
            session['win_rate_per_hour'] = session['total_profit'] / session['total_hours']
        else:
            session['win_rate_per_hour'] = None
    
    fig = px.line(
        x=[s.date for s in sessions],
        y=[s.win_loss for s in sessions],
        title='Overall Stats',
        labels={'x': 'Date', 'y': 'Win/Loss'}
    )
    fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='green', size=14))
    fig.update_layout(title={
        'font_size': 22,
        'xanchor': 'center',

        'x': 0.5
    })
    fig.update_layout(
        autosize=True)
    
    chart = fig.to_html()
        
    context = {'chart': chart,
        'overall_hourly_rate': overall_hourly_rate,
        'overall_hours': overall_hours,
        'overall_total': overall_total,
        'current_month': current_month,
        'current_year': current_year,
        'sessions_by_month': sessions_by_month,
        'stakes_filter': stakes_filter,
            }
    return render(request, 'poker/index.html', context)


@login_required
def add_session(request):
    notes = SessionNotes.objects.all()
    if request.method == 'POST':
        form = PokerSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.player = request.user
            session.save()
            return redirect('poker:session_list')
    else:
        form = PokerSessionForm()

    return render(request, 'poker/add_session.html', {'form': form, 'notes': notes})

@login_required
def edit_session(request, session_id):
    session = get_object_or_404(PokerSession, id=session_id, player=request.user)

    if request.method == 'POST':
        form = PokerSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('poker:session_detail', session_id=session_id)
    else:
        form = PokerSessionForm(instance=session)

    context = {
        'form': form,
        'session': session,
    }

    return render(request, 'poker/session_edit.html', context)

@login_required
def session_detail(request, session_id):
    session = get_object_or_404(PokerSession, id=session_id, player=request.user)
    try:
        hands = Hands.objects.filter(session_id=session_id)
    except Hands.DoesNotExist:
        hands = None  # Set hands to None if no hands are found for the session

    context = {
        "session": session,
        "hands": hands
        
    }
    return render(request, 'poker/session_detail.html', context)

@login_required
def session_list(request):
    current_month = timezone.now().month
    current_year = timezone.now().year
    requested_month = int(request.GET.get('month', current_month))
    requested_year = int(request.GET.get('year', current_year))

    
    sessions = PokerSession.objects.filter(player=request.user, date__month=requested_month, date__year=requested_year)
    overall_total = sum(session.win_loss for session in sessions)
    overall_hours = sum(session.hours for session in sessions)
    overall_hourly_rate = overall_total / overall_hours if overall_hours > 0 else 0

    return render(request, 'poker/session_list.html', {
        'sessions': sessions,
        'overall_hourly_rate': overall_hourly_rate,
        'overall_total': overall_total,
        'current_month': current_month,
        'current_year': current_year,
    })

@login_required
def session_list_by_month(request):
    stakes_filter = request.GET.get('stakes')
    sessions = PokerSession.objects.filter(player=request.user)

    if stakes_filter:
        sessions = sessions.filter(stakes=stakes_filter).order_by('-created')

    # Calculate totals per month
    sessions_by_month = sessions.annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        total_profit=Sum('cash_out') - Sum('buy_in'),  # Calculate total profit/loss
        total_hours=Sum('hours')  # Sum of hours
    ).order_by('-month')

    # Calculate total wins/losses and hourly rate for each month
    for session in sessions_by_month:
        # Calculate win rate per hour
        if session['total_hours']:
            session['win_rate_per_hour'] = session['total_profit'] / session['total_hours']
        else:
            session['win_rate_per_hour'] = None
        
        # Add total wins/losses to each session entry
        session['total_wins_losses'] = session['total_profit']

    context = {
        'sessions_by_month': sessions_by_month,
        'stakes_filter': stakes_filter,
    }

    return render(request, 'poker/session_list_by_month.html', context)

#Notes Model Section

@login_required
def add_session_note(request, session_id):
    poker_session = get_object_or_404(PokerSession, id=session_id)
   

    if request.method == 'POST':
        form = SessionNotesForm(request.POST)
        if form.is_valid():
            session_note = form.save(commit=False)
            session_note.pokersession = poker_session  # Associate note with session
            session_note.save()
            return redirect('poker:session_detail', session_id=session_id)
    else:
        form = SessionNotesForm()

    return render(request, 'poker/note_add.html', {'form': form, 'poker_session': poker_session})


@login_required
def edit_session_note(request, note_id, session_id):
    # Get the existing session note by its ID
    session_note = get_object_or_404(SessionNotes, id=note_id)
    poker_session = get_object_or_404(PokerSession, id=session_id)

    # If the request is POST, process the form data
    if request.method == 'POST':
        form = SessionNotesForm(request.POST, instance=session_note)
        if form.is_valid():
            form.save()
            # Redirect to session detail view after saving
            return redirect('poker:session_detail', session_id=session_id)
    else:
        form = SessionNotesForm(instance=session_note)  # Pre-populate with existing data

    return render(request, 'poker/note_edit.html', {
        'form': form,
        'session_note': session_note,
        'poker_session': poker_session
    })

@login_required
def session_notes_list(request):
    query = request.GET.get('q', '')
    notes = SessionNotes.objects.all()

    if query:
        notes = notes.filter(Q(notes__icontains=query) | Q(takeaway__icontains=query))

    context = {
        'notes': notes,
        'query': query,
    }
    return render(request, 'poker/notes_list.html', context)

# Charts and Graphs

@login_required
def overall_chart(request):
    session = PokerSession.objects.filter(player=request.user)

    # Get filter parameters from the request
    start = request.GET.get('start')
    end = request.GET.get('end')
    stakes = request.GET.get('stakes')

    # Apply filters to the queryset
    if start:
        session = session.filter(date__gte=start)
    if end:
        session = session.filter(date__lte=end)
    if stakes:
        session = session.filter(stakes=stakes)

    # Sort sessions by date to ensure proper chronological order
    session = session.order_by('date')

    # Calculate cumulative win/loss (cash_out - buy_in)
    win_loss = []  # Win/Loss for the x-axis
    dates = []     # Dates for the y-axis
    for s in session:
        session_win_loss = s.cash_out - s.buy_in
        win_loss.append(session_win_loss)
        dates.append(s.date)

    # Create the rotated bar chart
    fig = px.bar(
        y=win_loss,  # Use win/loss values for y-axis (inverted axis)
        x=dates,     # Use dates for x-axis (inverted axis)
        orientation='v',  # Vertical bar chart (inverted orientation)
        title='Overall Win/Loss per Session',
        labels={'x': 'Date', 'y': 'Win/Loss'}
    )

    # Style the plot
    fig.update_layout(
        title={
            'font_size': 22,
            'xanchor': 'center',
            'x': 0.5
        },
        xaxis=dict(
            automargin=True
        )
    )

    # Convert the plot to HTML
    chart = fig.to_html()

    # Render the template with the chart
    context = {'chart': chart, 'form': DateForm()}
    return render(request, 'poker/overall_chart.html', context)