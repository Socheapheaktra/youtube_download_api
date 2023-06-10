from flask_smorest import Blueprint, abort
from flask.views import MethodView
from pytube import Search, YouTube, Playlist
from flask import send_file

import os

from models import YoutubeModel
from schemas import YoutubeSchema, YoutubePlaylistSchema, YoutubeSearchSchema

blp = Blueprint("Youtube Downloader", __name__, description="Operation on YoutubeDownloader")

@blp.route("/search")
class SearchByLink(MethodView):
    @blp.arguments(YoutubeSearchSchema)
    @blp.response(200, YoutubeSearchSchema)
    @blp.doc(
        summary="Get list of Youtube Object by 'video_title' (Can also pass Youtube Link to search for specific video)",
        description="Return Data of Youtube Video based on given title",
    )
    def post(self, req_data):
        title = req_data['search_query']
        try:
            yt = Search(f'{title}')
            data = [
                YoutubeModel(
                    author=item.author,
                    length=item.length if item.length else None,
                    publish_date=item.publish_date,
                    thumbnail_url=item.thumbnail_url,
                    title=item.title,
                    video_id=item.video_id,
                    views=item.views if item.views else None
                ).to_json() for item in yt.results
            ]
            response = {
                "search_query": req_data['search_query'],
                "item_count": len(data),
                "page": 1,
                "results": data
            }
        except Exception as err:
            abort(500, message=f"{err}")
        else:
            return response

@blp.route("/search/<string:video_id>")
class SearchByID(MethodView):
    @blp.response(200, YoutubeSchema)
    @blp.doc(
        summary="Fetch Youtube Object by ID",
        description="Return Data of Youtube Object based on the given 'video_id'",
    )
    def get(self, video_id):
        try:
            yt = YouTube.from_id(video_id)
            data = YoutubeModel(
                author=yt.author,
                length=yt.length,
                publish_date=yt.publish_date,
                thumbnail_url=yt.thumbnail_url,
                title=yt.title,
                video_id=yt.video_id,
                views=yt.views
            )
        except Exception as err:
            abort(500, message=f"{err}")
        else:
            return data.to_json()

@blp.route('/search/playlist')
class SearchPlaylist(MethodView):
    @blp.arguments(YoutubePlaylistSchema)
    @blp.response(200, YoutubeSchema(many=True))
    @blp.doc(summary="Fetch Youtube Playlist By Link",
             description="Return List of Youtube Object based on the Playlist Link")
    def post(self, req_data):
        try:
            playlist = Playlist(req_data['playlist_link'])
            data = [
                YoutubeModel(
                    author=video.author,
                    length=video.length,
                    publish_date=video.publish_date,
                    thumbnail_url=video.thumbnail_url,
                    title=video.title,
                    video_id=video.video_id,
                    views=video.views
                ).to_json() for video in playlist.videos
            ]
        except Exception as err:
            abort(500, message=f"{err}")
        else:
            return data
        
@blp.route('/download/mp4/<string:video_id>')
class DownloadVideo(MethodView):
    @blp.doc(
        summary="Download Video based on the given (video_id)",
        description="Return an mp4 file of the (video_id)",
    )
    def get(self, video_id):
        try:
            # Download the video using pytube
            video = YouTube.from_id(video_id=video_id)
            stream = video.streams.get_highest_resolution()
            video_file = stream.download()

            # Return the temporary file as an API response
            response = send_file(
                video_file, 
                as_attachment=True,
                download_name=f"{video.title}.mp4"
            )
        except Exception as err:
            os.remove(video_file)
            abort(500, message=f"{err}")
        else:
            # remove file from server storage
            os.remove(video_file)
            return response
        
@blp.route('/download/mp3/<string:video_id>')
class DownloadAudio(MethodView):
    @blp.doc(
        summary="Download Audio based on the given (video_id)",
        description="Return an mp3 file of the given (video_id)",
    )
    def get(self, video_id):
        try:
            # Download the video using pytube
            video = YouTube.from_id(video_id=video_id)
            stream = video.streams.get_audio_only()
            audio_file = stream.download()

            # Return the temporary file as an API response
            response = send_file(
                audio_file, 
                as_attachment=True,
                download_name=f"{video.title}.mp3"
            )            
        except Exception as err:
            abort(500, message=f"{err}")
        else:
            # remove file from server storage
            os.remove(audio_file)
            return response