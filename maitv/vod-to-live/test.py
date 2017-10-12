from vodtolive import HLSVod

def main():
	vod = HLSVod('http://dw2nch8cl472k.cloudfront.net/HLS/Apple%20HLS/HTTP%20example.m3u8')
	vod.dump()
	print "LIST PLAYLISTS"
	vod.list_playlists()

	print "GET SEGMENT for bitrate 18830456"
	vod.get_segment('18830456')
	#print "GET SEGMENT for bitrate 42191"
	#vod.get_segment('42191')


	vod.get_segment2()
	
	print('VOD NEXT STARTS')
	vod.next()
	print('VOD NEXT ENDS')

if __name__ == '__main__':
	try:
		main()
	except Exception, err:
		raise