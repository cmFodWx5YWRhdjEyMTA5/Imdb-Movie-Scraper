from bs4 import BeautifulSoup
import requests,pprint

url = "https://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in"
page = requests.get(url)
soup = BeautifulSoup(page.text,'html.parser')

#Task1
# Here we scrap the list of 250 movies data.
def scrap_top_list():
	main_div = soup.find('div', class_='lister')
	tbody = main_div.find('tbody', class_='lister-list')
	trs = tbody.find_all('tr')

	movie_ranks =[]
	movie_name = []
	year_of_realease = []
	movie_urls = []
	movie_ratings = []

	for tr in trs:
		# Here we scrap ranks of movies. 
		position = tr.find('td', class_ ="titleColumn").get_text().strip()
		rank = ''
		for i in position:
			if '.' not in i:
				rank = rank + i	
			else:
				break
		movie_ranks.append(rank)
		
		# Here we scrap movie name or movie title	
		title = tr.find('td', class_ ="titleColumn").a.get_text()
		movie_name.append(title)

		# Here we scrap year of movie released.
		year = tr.find('td',class_ = "titleColumn").span.get_text()
		year_of_realease.append(year)

		# Here we scrap imdb ratings of movies.
		imdb_rating = tr.find('td',class_="ratingColumn imdbRating").strong.get_text()
		movie_ratings.append(imdb_rating)

		# Here we scrap movies urls or links.
		link = tr.find('td', class_="titleColumn").a['href']
		movie_link = "https://www.imdb.com" + link
		movie_urls.append(movie_link)

	Top_Movies = []
	movie_details ={'position':'','name':'','year':'','rating':'','url':''}
	for i in range(0,len(movie_ranks)):
		movie_details['position'] = int(movie_ranks[i])
		movie_details['name'] = str(movie_name[i])
		year_of_realease[i] = year_of_realease[i][1:5]
		movie_details['year'] = int(year_of_realease[i])
		movie_details['rating'] = float(movie_ratings[i])
		movie_details['url'] = movie_urls[i]
		Top_Movies.append(movie_details)
		movie_details ={'position':'','name':'','year':'','rating':'','url':''}
	return (Top_Movies)
scrap = scrap_top_list()
#pprint.pprint(scrap)
#print(scrap)

#Task2
# Here the parameter movies is the dic type which is output of scrap_top_list() function 
# Here we passed the scrap as argument in this function.
def group_by_year(movies):
	years = []
	movie_dict = {}
	for i in movies:
		year = i['year']
		if year not in years:
			years.append(year)
	for i in years:
		movie_dict[i] = []
	return movie_dict
# pprint.pprint(group_by_year(scrap))
# print(group_by_year(scrap))

#Task3
# Here the parameter movies is the dic type which is output of scrap_top_list() function 
# Here we passed the scrap as argument in this function.
def group_by_decade(movies):
	movies_by_year = group_by_year(movies)
	movie_decade = {}
	decade_list = []

	# Here we get the keys of group_by_year() function which is years of movies
	for keys in movies_by_year:
		reminder = keys % 10
		subtract = keys - reminder
		if subtract not in decade_list:
			decade_list.append((subtract))
	decade_list.sort()

	# Here we created movie_decade dic and assigning the empty list to it.
	for decades in decade_list:
		movie_decade[decades] = []

	# Here we assiging the value to movie_decade dic
	for i in movie_decade:
		for j in movies_by_year:
			if j in range(i,i+10):
				movie_decade[i] += movies_by_year[j]
	return movie_decade
	#pprint.pprint(movie_decade)
# print(group_by_decade(scrap))

# Task 4
def scrap_movie_details(movie_url):
	page = requests.get(movie_url)
	soup = BeautifulSoup(page.text,'html.parser')

	# Here I scrap movie name
	title_div = soup.find('div',class_="title_wrapper").h1.get_text()
	movie_name = ''
	for i in title_div:
		if '(' not in i:
			movie_name = (movie_name + i).strip()
		else:
			break

	# In this div where I get all the other things like runtime,gener and more
	sub_div  = soup.find('div',class_="subtext")
	
	# Here I scrap movie runtime.
	runtime = sub_div.find('time').get_text().strip()
	runtime_hours = int(runtime[0])*60
	if 'min' in sub_div:
		runtime_minutes = int(movie_runtime[3:].strip('min'))
		movie_runtime = runtime_hours + runtime_minutes
	else:
		movie_runtime = runtime_hours 

	# Here I scrap movie gener.
	gener = sub_div.find_all('a')
	gener.pop()
	movie_gener = [i.get_text() for i in gener]

	# In This div i get movie bio and movie director
	summary = soup.find('div', class_="plot_summary")

	# Here I scrap movie bio
	movie_bio = summary.find('div', class_="summary_text").get_text().strip()

	# Here I scrap director of the movie.
	director = summary.find('div', class_="credit_summary_item")
	director_list = director.find_all('a')
	movie_directors = [i.get_text().strip() for i in director_list]

	# In this div i get country and language details.
	extra_details = soup.find('div', attrs={"class":"article","id":"titleDetails"})
	list_of_divs = extra_details.find_all('div')
	for div in list_of_divs:
		tag_h4 =  div.find_all('h4')
		for text in tag_h4:
			if 'Language:' in text:
				tag_anchor = div.find_all('a')
				movie_language = [language.get_text() for language in tag_anchor]
			elif 'Country:' in text:
				tag_anchor = div.find_all('a')
				movie_country = ''.join([country.get_text() for country in tag_anchor])

	# Here I scrap Poster Image_Url.
	movie_poster_link = soup.find('div', class_="poster").a['href']
	movie_poster= "https://www.imdb.com" + movie_poster_link

	# Here I create Dic for movie-details
	movie_detail_dic = {'name':'','director':'','bio':'','runtime':'','gener':'','language':'','country':'','poster_img_url':''}

	movie_detail_dic['name'] = movie_name
	movie_detail_dic['director'] = movie_directors
	movie_detail_dic['bio'] = movie_bio
	movie_detail_dic['runtime'] = movie_runtime
	movie_detail_dic['gener'] = movie_gener
	movie_detail_dic['language'] = movie_language
	movie_detail_dic['country'] = movie_country
	movie_detail_dic['poster_img_url'] = movie_poster

	return movie_detail_dic

url1 = scrap[0]['url']
movie_detail = scrap_movie_details(url1)
#print(movie_detail)

# Task 5
def get_movie_list_details(movies):
	movie_list = []
	for i in movies:
	 	urls = i['url']
	 	a = scrap_movie_details(urls)
	 	movie_list.append(a)
	return movie_list
first_twenty_movies = get_movie_list_details(scrap[:20])
# print(first_twenty_movies)


# Task 6
def analyse_movies_language(movies):
	language_list = []
	for i in movies:
		a = i['language']
		for j in a:
			if j not in language_list:
				language_list.append(j)
	analyse__language ={lang:0 for lang in language_list} 
	for lang in language_list:
		for movie in movies:
			if lang in movie['language']:
				analyse__language[lang] +=1
	return analyse__language

language_analyse = analyse_movies_language(first_twenty_movies)
#print(language_analyse)

# Task7
def analyse_movies_directors(movies):
	director_list = []
	for i in movies:
		a = i['director']
		for j in a:
			if j not in director_list:
				director_list.append(j)
	analyse__director ={director:0 for director in director_list} 
	for director in director_list:
		for movie in movies:
			if director in movie['director']:
				analyse__director[director] +=1
	return analyse__director
director_analyse = analyse_movies_directors(first_twenty_movies)
# print(director_analyse)

# Extra Bonus Task
def get_see_full_cast_url(movie_url):
	# From this function I scrap the see_full_cast link urls from movie details page.
	html_doc = requests.get(movie_url)
	soup = BeautifulSoup(html_doc.text,'html.parser')

	# Here I call extract_movie_detail and get poster_img_url
	movie = scrap_movie_details(movie_url)
	imgae_url = movie['poster_img_url']
	movie_name = movie['name']

	# Here I scrap cast url.
	movie_details = soup.find('div', attrs={"class":"article","id":"titleCast"})
	cast_main_div = movie_details.find('div', class_="see-more").a['href']
	cast_url = imgae_url[:37] + cast_main_div

	cast_html = requests.get(cast_url)
	cast_soup = BeautifulSoup(cast_html.text,'html.parser')

	detail_list = []

	# Here I scrap movie name and Cast details.
	main_div = cast_soup.find('div', class_='article listo')
	movie_name = main_div.find('div',class_='parent').h3.a.get_text()
	cast_table = main_div.find('table', class_='cast_list')
	cast_table_trs = cast_table.find_all('tr')
	# cast_table_trs.pop(0)
	for tr in cast_table_trs:
		cast_tds = tr.find_all('td')
		if len(cast_tds) > 1:
			cast_name = cast_tds[1].a.get_text().strip('\n')
			detail_list.append(cast_name.strip())
	cast_dic = {movie_name:detail_list}
	return cast_dic

url2 = scrap[2]['url']
cast_full_detail = get_see_full_cast_url(url2)
# print(cast_full_detail)
