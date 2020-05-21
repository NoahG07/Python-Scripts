#!/usr/bin/env python

try: 
    import urllib.request
    from urllib.parse import urlparse
    import bs4 as bs 
    import sys, subprocess, os, zipfile
except ModuleNotFoundError as e:
    print("[*] Error: ", e)
    sys.exit()

def search_subs():
    # entering 'movie name' into url 
    url = "http://www.yifysubtitles.com/search?q=" 
    movie_name = input("[*] Search for: ")  
    movie_fix = movie_name.lower().replace(" ", "+") 

    # Getting connection to website
    movie_url = url + movie_fix 
    source = urllib.request.urlopen(movie_url).read() 
    soup = bs.BeautifulSoup(source, "html.parser") 

    # Searches through a table of movies
    movie_dict = {} # 'title':'url'
    movie_list = []
    tables = soup.findAll("li", {"class": "media media-movie-clickable"}) 

    for table in tables: 
        # Goes to media-body of the container
        media_body = table.findAll("div", {"class":"media-body"}) 
        media_body = media_body[0] 

        # Finding movie subtitle URL
        # finds movie/subtitle sub-link 
        sub_link = media_body.findAll("a") 
        sub_link = sub_link[0] 
        link = sub_link.get("href") 

        # parses the original url 
        parse_obj = urlparse(movie_url) 
        url = parse_obj.scheme + "://" + parse_obj.netloc 
        sub_url = url + link 

        # Finds the movie title
        movie_title = media_body.findAll("h3", {"itemprop":"name"}) 
        movie_title = movie_title[0] 
        title = movie_title.string 

        # Finds the year of the movie
        years = media_body.findAll("span", {"class":"movinfo-section"})[0] 
        year = years.contents[0]

        movie_year = f"{title} ({year})"
        movie_dict[movie_year] = sub_url

    # copies dictionary items into a list
    for m in movie_dict.items():
        movie_list.append(m)

    # enumerating list and prints titles    
    for k, v in enumerate(movie_list):
        print(f"{k}) {v[0]}")

    select_url = input("\nSelect the movie: ")

    # Enumerates list again and allows selection from count
    for k, v in enumerate(movie_list):
        if int(select_url) == k:
            # v[1] is the movie url
            my_url = v[1]
            # movie_url is the function argument
            download(my_url)

def download(my_url):
    # Opens The YIFY Subtitle Website To Be Read
    source = urllib.request.urlopen(my_url).read()
    soup = bs.BeautifulSoup(source, "html.parser")

    # Gets Movie Name
    title_sub = soup.title.string

    # Variable for Subtitle Table
    table_subs = soup.find("table", {"class": "table other-subs"}).findAll("tr")

    # The First List In The Table Is Useless
    useless = table_subs.pop(0)

    # Makes A List For The English Rows
    tabs = []

    # Searches Through The Tabe For The First English Subtitles.
    for table in table_subs:
        if table.find("span", {"class": "sub-lang"}).string == "English":
            tabs.append(table)

    # Uses The First Subtitle Class Because It IS The Highest Rating Subtitle
    my_subs = tabs[0]

    # Finds The Subtitle URL
    sub_link = my_subs.findAll("a")[0]
    link = sub_link.get("href")

    # Makes A Variable For The Subtitle URL
    parse_obj = urlparse(my_url)
    url = parse_obj.scheme + "://" + parse_obj.netloc
    sub_url = url + link

    # Opens The Subtitle URL To Be Read
    source = urllib.request.urlopen(sub_url).read()
    soup = bs.BeautifulSoup(source, "html.parser")

    # Variable For The Zip URL
    zip_url = soup.findAll("a", {"class": "btn-icon download-subtitle"})
    z_url = zip_url[0]
    files = z_url.get("href")

    # Parses ONLY The File Name NOT The URL
    movie_url = urlparse(files)
    movie_path = movie_url.path
    movie = movie_path.replace("/subtitle/", "")

    if not os.path.isdir("subtitles"):
        os.mkdir("subtitles")
        os.chdir("subtitles")
    else:
        os.chdir("subtitles")

    if not os.path.isfile(movie):
        print(f"\nDownloading {title_sub}...")
        subprocess.run(["curl", "-O", files])
        zip_extraction()
    else:
        print(f"\nAlready Exists: {title_sub}")
        zip_extraction()

def zip_extraction():
    if os.path.isdir("subtitles"):
        os.chdir("subtitles")

    for file in os.listdir("."):
        if zipfile.is_zipfile(file):
            with zipfile.ZipFile(file) as fzip:
                for f in fzip.namelist():
                    if f.endswith(".srt"):
                        try:
                            print(f"\nExtracting: {f}")
                            fzip.extract(f)
                        except:
                            print("\nCould not extract files!")
                    else:
                        sys.exit()
            os.remove(file)
            sys.exit()

if __name__ == "__main__":
    search_subs()
