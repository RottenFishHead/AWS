from django.urls import path
from poker.views import (
                         index,
                         add_session, 
                         edit_session,
                         session_list, 
                         session_detail,
                         session_list_by_month, 
                         overall_chart,
                         index,
                         add_session_note,
                         edit_session_note,
                         session_notes_list

                         )

app_name = 'poker' 


urlpatterns = [
    path('', index, name='home'),
    path('sessions/', session_list, name='session_list'),
    path('sessions/add/', add_session, name='add_session'),
    path('session/edit/<int:session_id>/', edit_session, name='edit_session'),
    path('session_detail/<int:session_id>/', session_detail, name='session_detail'),
    path('session/<int:session_id>/add-note/', add_session_note, name='add_session_note'),
    path('session/<int:session_id>/note/<int:note_id>/edit/', edit_session_note, name='edit_session_note'),
    path('sessions-by-month/', session_list_by_month, name='session_list_by_month'),
    path('chart/', overall_chart, name='overall_chart'),
    path('session/<int:session_id>/add-note/', add_session_note, name='add_session_note'),
    path('session/<int:session_id>/note/<int:note_id>/edit/', edit_session_note, name='edit_session_note'),
    path('session-notes/', session_notes_list, name='session_notes_list'),
    
 
]



