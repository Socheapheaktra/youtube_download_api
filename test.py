from pytube import Search

s = Search("https://www.youtube.com/watch?v=Tv40mcAM1ZA")


print(s.fetch_and_parse())
