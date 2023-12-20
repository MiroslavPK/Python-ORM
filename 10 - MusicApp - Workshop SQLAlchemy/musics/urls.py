from musics import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path('album/', include([
        path('create/', views.create_album, name='create album'),
        path('details/<int:id>', views.details_album, name='album details'),
        path('edit/<int:id>', views.edit_album, name='edit album'),
        path('delete/<int:id>', views.delete_album, name='delete album'),
    ])),
    path('song/', include([
        path('create/', views.create_song, name='create song'),
        path('play/<int:album_id>/<int:song_id>', views.play_song, name='play song'),
        path('serve_song/<int:album_id>/<int:song_id>', views.serve_song, name='serve song')
]))]