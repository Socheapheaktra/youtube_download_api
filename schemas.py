from marshmallow import Schema, fields

class YoutubeSchema(Schema):
    author = fields.Str(dump_only=True)
    length = fields.Int(dump_only=True, allow_none=True)
    publish_date = fields.Str(dump_only=True)
    thumbnail_url = fields.Str(dump_only=True)
    title = fields.Str(dump_only=True)
    video_id = fields.Str(dump_only=True)
    views = fields.Int(dump_only=True, allow_none=True)
    
class YoutubePlaylistSchema(Schema):
    playlist_link = fields.Str(load_only=True, required=True)
    author = fields.Str(dump_only=True)
    length = fields.Int(dump_only=True, allow_none=True)
    publish_date = fields.Str(dump_only=True)
    thumbnail_url = fields.Str(dump_only=True)
    title = fields.Str(dump_only=True)
    video_id = fields.Str(dump_only=True)
    views = fields.Int(dump_only=True, allow_none=True)
    
class YoutubeSearchSchema(Schema):
    search_query = fields.Str(required=True)
    item_count = fields.Int(dump_only=True)
    page = fields.Int(dump_only=True)
    results = fields.List(fields.Nested(YoutubeSchema), dump_only=True)
