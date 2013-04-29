# Display categories by mood
@app.route("/mood/<mood_name>")
def by_mood(mood_name):

	# get the first 3 interests inside Experience
	ints = models.Experience.objects.fields(slice__interest=[0,2])

	interest = ()

	for i in ints:

		interest = 'i'
		# get the last experience of a specific interest
		exp_highlight = models.Experience.objects(interest=interest).order_by('-timestamp')


	# try and get experiences where mood_name is inside the mood list
	try:
		experiences = models.Experience.objects(mood=mood_name)

	# not found, abort w/ 404 page
	except:
		abort(404)

	# prepare data for template
	templateData = {
		'current_mood' : {
			'slug' : mood_name,
			'name' : mood_name.replace('_',' ')
		},
		'experiences' : experiences,
		'mood' : mood,
		'interest' : interest,
		'exp_highlight' : exp_highlight,
		'ints' : ints,
	}

	if mood_name == "Zippy":

		# render and return template
		return render_template('04mood_listing01.html', **templateData)

	if mood_name == "Chill":


		return render_template('04mood_listing02.html', **templateData)

	if mood_name == "Hungry":

		return render_template('04mood_listing03.html', **templateData)

	else: 

		return render_template('04mood_listing04.html', **templateData)


