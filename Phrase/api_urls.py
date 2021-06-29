from django.urls import path

from Phrase import api_views

urlpatterns = [
    path('tag', api_views.TagView.as_view()),
    path('phrase', api_views.PhraseView.as_view()),
]
