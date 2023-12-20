from django.shortcuts import render, redirect, HttpResponse
from musics.models import Album, Song
from common.session_decorator import session_decorator
from musicApp.settings import session
from musics.forms import AlbumCreateForm, AlbumEditForm, AlbumDeleteForm, SongCreateForm


@session_decorator(session)
def index(request):
    albums = session.query(Album).all()
    
    context = {
        'albums': albums
    }

    return render(request, 'common/index.html', context=context)


@session_decorator(session)
def create_album(request):
    if request.method == 'POST':
        form = AlbumCreateForm(request.POST)
        
        if form.is_valid():
            new_album = Album(
                album_name = form.cleaned_data['album_name'],
                image_url = form.cleaned_data['image_url'],
                price = form.cleaned_data['price'],
            )

            session.add(new_album)

        return redirect('index')
    else:
        context = {
            'form': AlbumCreateForm()
        }
        
        return render(request, 'albums/create-album.html', context=context)


def details_album(request, id):
    album = session.query(Album).filter(Album.id == id).first()

    context = {
        'album': album
    }

    return render(request, 'albums/album-details.html', context = context)


@session_decorator(session)
def edit_album(request, id):
    album = session.query(Album).filter(Album.id == id).first()

    if request.method == 'POST':
        form = AlbumEditForm(request.POST)

        if form.is_valid():
            album.album_name = form.cleaned_data['album_name']
            album.image_url = form.cleaned_data['image_url']
            album.price = form.cleaned_data['price']

            return redirect('index')

    else:
        initial_data = {
            'album_name': album.album_name,
            'image_url': album.image_url,
            'price': album.price,
        }

        form = AlbumEditForm(initial=initial_data)

    context = {
        'form': form,
        'album': album
    }

    return render(request, 'albums/edit-album.html', context=context)


@session_decorator(session)
def delete_album(request, id):
    album = session.query(Album).filter(Album.id==id).first()

    if request.method == 'POST':
        session.delete(album)

        return redirect('index')

    else:
        initial_data = {
            'album_name': album.album_name,
            'image_url': album.image_url,
            'price': album.price,
        }

        form = AlbumDeleteForm(initial=initial_data)

        for field in form.fields.values():
            field.widget.attrs['disabled'] = True

    context = {
        'form': form,
        'album': album
    }

    return render(request, 'albums/delete-album.html', context=context)


@session_decorator(session)
def create_song(request):
    if request.method == 'POST':
        form = SongCreateForm(request.POST, request.FILES)

        if form.is_valid():
            new_song = Song(
                song_name = form.cleaned_data['song_name'],
                album_id = form.cleaned_data['album'],
                music_file = request.FILES['music_file'].read()
            )

            session.add(new_song)

        return redirect('index')

    # if request method is GET
    context = {
        'form': SongCreateForm()
    }
    
    return render(request, 'songs/create-song.html', context=context)



@session_decorator(session)
def play_song(request, album_id, song_id):
    song = session.query(Song).filter_by(
        id=song_id, 
        album_id = album_id
    ).first()

    album = session.query(Album).filter_by(
        id=album_id
    ).first()

    context = {
        'album': album,
        'song': song,
    }

    return render(request, 'songs/music-player.html', context=context)


@session_decorator(session)
def serve_song(request, album_id, song_id):
    song = session.query(Song).filter_by(
        id=song_id, 
        album_id = album_id
    ).first()

    if song:
        response = HttpResponse(song.music_file, content_type='audio/mpeg')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(song.song_name)
        return response
    else:
        return HttpResponse('Song not found', status=404)