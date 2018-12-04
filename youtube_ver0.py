from pytube import YouTube,Playlist
from pytube.exceptions import RegexMatchError
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re,os
#https://www.youtube.com/watch?v=-V0wIUQsFC8
def process_bar(stream = None, chunk = None, file_handle = None, remaining = None):
	i = int((file_size - remaining) / file_size * 10)
	percent = (file_size - remaining) / file_size * 100
	process = 'Song : ' + display_name + ' [' + '>' * i + ' ' * (10 - i) + ']' + "%.2f" % percent + '%'
	print(process,end = '\r',flush = True)
def name_producer(filename):
	if len(filename) > 20:
		return filename[:17] + '...'
	else:
		return filename[:len(filename) - 4]
def song_downloader(link,path):
	try:
		mp4_filename = YouTube(link).streams.first().default_filename
		if not os.path.exists(os.path.join(path,mp4_filename[:len(mp4_filename) - 4] + '.mp3')):
			global display_name
			display_name = name_producer(mp4_filename)
			print('Song : ' + display_name,end = '\r',flush = True)
			data = YouTube(link,on_progress_callback = process_bar).streams.filter(only_audio = True).first()	
			global file_size
			file_size = data.filesize
			data.download(path)
			os.rename(os.path.join(path,mp4_filename),os.path.join(path,mp4_filename[:len(mp4_filename) - 4] + '.mp3'))
			print(' ' * 60,end = '\r',flush = True)
			print('Song : ' + display_name + ' [OK]')
		else:
			print("You have already download this song")
	except RegexMatchError:
		print("Error : Invalid Link")
def promote(msg):
	true_list = {'yes','y',''}
	false_list = {'no','n'}
	choice = input('{}'.format(msg)).lower()
	if choice in true_list:
   		return True
	elif choice in false_list:
   		return False
	else:
   		sys.stdout.write("Error : Invalid response")
   		promote(msg)
def main():
	link = str(input("Link : "))
	if re.search(r"list",link):
		for _ in re.split(r"[?&]",link):
			if 'list' in _ and 'playlist' not in _:
				link = 'https://www.youtube.com/playlist?' + _
				break
		bs = BeautifulSoup(urlopen(link).read(),"html.parser")
		listname = bs.find("h1",{"class":"pl-header-title"}).get_text().strip()
		print("Playlist : " + listname)
		data = Playlist(link).parse_links()
		link_list = []
		for _ in data:
			link_list += ['https://www.youtube.com' + _]
		new_path = path + '\\' + listname
		if not os.path.exists(new_path):
			os.makedirs(new_path)
		else:
			os.makedirs(new_path + '(1)')
		for _ in link_list:
			song_downloader(_,new_path)
	else:
		song_downloader(link,path)
	if promote("Download another song?(Y/N)"):
		main()
	else:
		print("Thank for using!!!")
###############################################################
print("""
##########################################################
######                                             #######
###### ########## ########## ########## ########## #######
###### ########## ########## ########## ########## #######
###### ########## ########## ########## ########## #######
###### ########## ########## ########## ########## #######
###    ########   ########   ########   ########   #######
###    ########   ########   ########   ########   #######
##########################################################
"""
)
path = "C:\\Users\\tequi\\Downloads"
main()