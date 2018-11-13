from django.urls import path

from Phrase.api_views import TagView, PhraseView

urlpatterns = [
    path('tag', TagView.as_view()),
    path('phrase', PhraseView.as_view()),
]