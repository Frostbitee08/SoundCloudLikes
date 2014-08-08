import soundcloud, webbrowser, urllib, json, os, sys, time
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TRCK, TIT2, TPE1, TALB, TDRC, TCON, COMM, APIC, error

print sys.argv
os.chdir(sys.argv[1])

Excpetions = open('Excpetions.txt', 'a')
#Dates = open('SoundCloudLikes.txt', 'r')

#Fill in your user name and password
client = soundcloud.Client(
    client_id='0c61ce131a2c1db8e56059446e33456a',
    client_secret='fe8e73e1113bc8d885c773cd63dabf1f',
    username='',
    password=''
)

#stamp = str(Dates.readline())
#stamp = "2014/08/04 18:40:08 +0000"

#Change the limit to however many songs you want
current_user = client.get('/me', g = 'keyword')
favorites = client.get('/me/favorites', limit=200)

#''', created_at={ 'from': stamp}'''

'''Dates.close()
Dates = open('SoundCloudLikes.txt', 'w')
Dates.write(time.strftime("%Y/%m/%d %H:%M:%S"))'''

for song in favorites:
	print song.title
	title = song.title
	artist = ""
	name = ""

	if "-" in title:
		index = title.index('-')-1
		artist = title[:index]
		name = title[index+2:]
	else:
		artist = song.user['username']
		name = song.title

	if name[0] == " ":
		name = name[1:]
		pass

	fileTitle = name + ".mp3"

	#Get Song Info
	waveform_url = song.waveform_url
	songCode = waveform_url[22:len(waveform_url)-6]
	url = "http://media.soundcloud.com/stream/" + songCode

	#Download Song
	save = True
	try:
		(filename, headers) = urllib.urlretrieve(url, fileTitle)
		pass
	except Exception, e:
		errorMessage = name + " : Exception", e
		print errorMessage
		errorMessage = str(errorMessage) + '\n'
		Excpetions.write(errorMessage)
		save = False
		pass

	if save:
		#Add Tags
		audio = MP3(fileTitle, ID3=ID3)
		if song.artwork_url is not None:
			artwork_url = song.artwork_url[:len(song.artwork_url)-17] + "t500x500.jpg"
		else:
			artwork_url = ""

		# add ID3 tag if it doesn't exist
		try:
		    audio.add_tags()
		except error:
		    pass

		if artwork_url != "":
			audio.tags.add(
			    APIC(
			        encoding=3, # 3 is for utf-8
			        mime='image/jpeg', # image/jpeg or image/png
			        type=3, # 3 is for the cover image
			        desc=u'Cover',
			        data=urllib.urlopen(artwork_url).read()
			    )
			)

		audio.tags.add(TIT2(encoding=3, text=name))
		audio.tags.add(TPE1(encoding=3, text=artist))
		audio.tags.add(TDRC(encoding=3, text=str(song.release_year)))
		audio.tags.add(TCON(encoding=3, text=song.genre))

		audio.save()

	pass

Excpetions.close()
#Dates.close()