class YoutubeModel:
    def __init__ (
        self,
        author: str,
        length: int,
        publish_date: str,
        thumbnail_url: str,
        title: str,
        video_id: str,
        views: int
    ):
        self.author = author
        self.length = length
        self.publish_date = publish_date
        self.thumbnail_url = thumbnail_url
        self.title = title
        self.video_id = video_id
        self.views = views
        
    def to_json(self) -> dict:
        return {
            "author": self.author,
            "length": self.length,
            "publish_date": self.publish_date.strftime("%Y-%m-%d"),
            "thumbnail_url": self.thumbnail_url,
            "title": self.title,
            "video_id": self.video_id,
            "views": self.views
        }
        
    def __str__(self) -> dict:
        return {
            "author": self.author,
            "length": self.length,
            "publish_date": self.publish_date,
            "thumbnail_url": self.thumbnail_url,
            "title": self.title,
            "video_id": self.video_id,
            "views": self.views
        }