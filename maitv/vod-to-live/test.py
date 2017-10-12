from vodtolive import HLSVod

def main():
	vod = HLSVod('http://dw2nch8cl472k.cloudfront.net/HLS/Apple%20HLS/HTTP%20example.m3u8')
	#vod.dump()
	#print "LIST PLAYLISTS"
	#vod.list_playlists()
	#print('HLS START')


	print "GET SEGMENT for bitrate 18830456"

	print vod.get_segment('18830456')

	print vod.get_segment('18830456')

	print vod.get_segment('18830456')

	print vod.get_segment('18830456')


if __name__ == '__main__':
	try:
		main()
	except Exception, err:
		raise