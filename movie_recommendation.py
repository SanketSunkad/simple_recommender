import requests
import json

def get_movies_from_tastedive(movieName, my_type):
    parameters = {}
    parameters["q"] = movieName
    parameters["type"] = my_type
    parameters["limit"] = 10
    apiUrl = "https://tastedive.com/api/similar"
    RecList = requests.get(apiUrl, params = parameters)
    return_data = json.loads(RecList.text)
    url_full = RecList.url
    return return_data

def extract_movie_titles(movieDict):
    titleList = []
    RecMovieList = movieDict["Similar"]["Results"]
    for movie in RecMovieList:
        titleList.append(movie["Name"])
    return titleList

def get_related_titles(userList, my_type):
    finalList = []
    for ul in userList:
        resp = get_movies_from_tastedive(ul, my_type)
        recMoviesList = extract_movie_titles(resp)
        for rcm in recMoviesList:
            if rcm not in finalList:
                finalList.append(rcm)

    return finalList

def get_movie_data(title):
    parameters = {}
    url = "https://www.omdbapi.com/"
    parameters["apikey"] = "yourkey"
    parameters["t"] = title
    parameters["r"] = "json"
    movieInfo = requests.get(url, parameters)
    info_dic = json.loads(movieInfo.text)
    return info_dic

def get_movie_rating(movie_dic):
    ratingList = movie_dic["Ratings"]
    b = [d["Value"] for d in ratingList if d["Source"]=="Rotten Tomatoes"]
    if len(b):
        rt = int(b[0].replace("%", ""))
        return (movie_dic["Title"], rt)
    else:
        return (movie_dic["Title"], 0)

def get_sorted_recommendations(userlist, my_type):
    final_rec_lt = get_related_titles(userlist, my_type)
    info_lt = []
    for movie in final_rec_lt:
        mv_info = get_movie_data(movie)
        info_lt.append(mv_info)
    rt_lt = []
    for info in info_lt:
        mv_rt = get_movie_rating(info)
        rt_lt.append(mv_rt)
    fl_rec_movies = [ m for m,r in sorted(rt_lt, key=lambda element: (element[1], element[0]), reverse=True)]
    return fl_rec_movies

my_type = input("Recommendation for movies or shows: \n").lower().split(",")
print(my_type)
    
mv_user_req = [item.strip() for item in input("Enter your favorite movies full title as given in IMDB separated by comas to get top recommendations to watch during your holidays: \n").split(",")]

mv_rec_final = get_sorted_recommendations(mv_user_req, my_type)
print("Watch the movies in below mentioned order you will love them")
print(mv_rec_final[:10])

#The documentation for the API is at https://tastedive.com/read/api.    
# The documentation for the API is at https://www.omdbapi.com/
# input example Bridesmaids, Sherlock Holmes

