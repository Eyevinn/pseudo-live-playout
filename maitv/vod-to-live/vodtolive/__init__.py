import m3u8


class HLSVod:
	def __init__(self, hlsManifestUri):
		self.hlsManifestUri = hlsManifestUri
		self.m3u8_obj = m3u8.load(self.hlsManifestUri)
		self.segments = {}

		print "HLSVOD Object"
		print self.m3u8_obj

		print "BASE URI"
		print self.m3u8_obj.base_uri

		for playlist in self.m3u8_obj.playlists:
			pth = self.m3u8_obj.base_uri + playlist.uri
			print "PLAYLIST URI: "
			print pth
			m3u8_playlist = m3u8.load(pth)
			for segment in m3u8_playlist.segments:
				key = str(playlist.stream_info.bandwidth)
				if not key in self.segments:
					self.segments[key] = [] 
				self.segments[key].append(segment)
				#print "KEYS"
				#print self.segments.keys()
				#print "Length"
				#print len(self.segments)
		self.index = 0

	def list_playlists(self):
		print self.m3u8_obj.playlists


	def list_bitrates(self):
		res = []
		#for key in self.segments.keys()
		#	res.append(key)
		#return res

	def next(self):
		self.index += 1
		#print(self.index)

	def get_segment(self, bitrate):
		res = ""

		res += self.m3u8_obj.base_uri + self.segments[bitrate] [self.index].uri    + "\n"
		res += self.m3u8_obj.base_uri + self.segments[bitrate] [self.index+1].uri  + "\n"
		next(self)

		return res
	

	def dump(self):
		print self.segments

		#for playlist in self.m3u8_obj.playlists:
		#	print playlist.uri


