## @package vodtolive

import m3u8
import os


def folderof(s):
	return os.path.dirname(s) + "/"
	
##	This class creates an object called HLSvod from an HLS (.m3u8) url 
#	and manipulates the HLS manifest from a VOD into a LIVE manifest. 
#	It creates a master playlist file and media playlist files 
#	from all given bitrates and returns them as strings
#	It also stitches together several urls to a master and media playlists
# 	so that the videos are played directly after each other
class HLSVod:

	## The constructor.
	#  Variables:
	#  hlsManifestUri - the provided url
	#  m3u8_obj - uses module m3u8 to create an object
	#  segments - all segments from the given url
	#  uris - urls to media playlists
	#  seg_count - counts all segments
	#
	def __init__(self, hlsManifestUri):
		self.hlsManifestUri = hlsManifestUri
		self.m3u8_obj = m3u8.load(self.hlsManifestUri)
		self.segments = {}
		self.uris = {}
		self.seg_count = 0
		self.playlength = 0

		for playlist in self.m3u8_obj.playlists:
			pth = self.m3u8_obj.base_uri + playlist.uri
			m3u8_playlist = m3u8.load(pth)
			for segment in m3u8_playlist.segments:
				key = str(playlist.stream_info.bandwidth)
				if not key in self.segments:
					self.uris[key] = folderof(pth)
					self.segments[key] = []
					self.seg_count = 0
					self.playlength = 0
				self.segments[key].append(segment)
				self.seg_count += 1
				self.playlength += segment.duration

	## Returns all media playlists from the given url
	def list_playlists(self):
		print self.m3u8_obj.playlists

	## Returns the available bitrates
	def list_bitrates(self):
		res = ""
		for btr in self.segments:
			res += str(btr) + ", "
		return res

	##	Returns the number of the given segment
	def get_segment_count(self):
		return self.seg_count
		
	def get_playlength(self):
		return self.playlength

	##	Returns the header section of a media playlist
	def get_header_lead(self, index):
		res = ""
		res += "#EXTM3U" + "\n"
		res += "#EXT-X-VERSION:3" + "\n"
		res += "#EXT-X-TARGETDURATION:4" + "\n"
		res += "#EXT-X-MEDIA-SEQUENCE:" + str(index) + "\n"
		return res;

	def get_header_normal(self):
		res = ""
		#res += "#EXTM3U" + "\n"
		#res += "#EXT-X-VERSION:3" + "\n"
		#res += "#EXT-X-TARGETDURATION:4" + "\n"
		return res;

	##	Returns a discontinuity tag, used when stitching together media playlist manifests
	def get_header_seam(self):
		res = ""
		#res += "#EXTM3U" + "\n"
		#res += "#EXT-X-VERSION:3" + "\n"
		#res += "#EXT-X-TARGETDURATION:4" + "\n"
		res += "#EXT-X-DISCONTINUITY-SEQUENCE" + "\n"
		#res += "#EXT-X-MEDIA-SEQUENCE:0\n"
		return res;

	## Returns a segment of a given bitrate and index.
	def get_segment(self, bitrate, index):
	
		if bitrate in self.segments:
			btr = bitrate
		else:
			fnd = False
			besf = 100.0
			fb = float(bitrate)
			for b in self.segments:
				er = abs((float(b)-fb) / fb)
				if not fnd:
					fnd = True
					btr = b
					besf = er
				else:
					if er < besf:
						fnd = True
						btr = b
						besf = er
	
		res = ""
		res += "#EXTINF:" + str(self.segments[btr][index].duration)  + "\n"
		res += self.uris[btr] + self.segments[btr][index].uri        + "\n"
		return res

	##	Returns and endlist tag to media playlist manifest, used when there are no more urls to play.
	def get_footer_end(self):
		res = ""
		res += "#EXT-X-ENDLIST\n"
		return res

	def dump(self):
		print self.segments

	## Returns live master manifest
	def get_live_master_manifest(self):
		master_manifest_string = ""
		master_manifest_string += "#EXTM3U" + "\n"
		counter = 0

		for playlist in self.m3u8_obj.playlists:
			master_manifest_string += "#EXT-X-STREAM-INF:" + "AVERAGE-BANDWIDTH="
			master_manifest_string += str(playlist.stream_info.average_bandwidth) + "," + "BANDWIDTH="
			master_manifest_string += str(playlist.stream_info.bandwidth) + "," + "CODECS=" + '"'
			master_manifest_string += playlist.stream_info.codecs + '"'
			newFileName = str(playlist.stream_info.bandwidth)
			if playlist.stream_info.resolution != None:
				master_manifest_string += ",RESOLUTION="
				resolution = ""
				for res in playlist.stream_info.resolution:
					resolution += str(res)
					master_manifest_string += str(res)
					if res != playlist.stream_info.resolution[-1]:
						master_manifest_string += "x"
						resolution += "x"
			else:
				newFileName = "audio"
			master_manifest_string += "\n" + newFileName + ".m3u8" + "\n"
			counter += 1

		return master_manifest_string

	## Returns live media manifest of a given bitrate
	def get_live_media_manifest(self, bitrate):
		media_manifest_string = ""
		media_manifest_string += "#EXTM3U" + "\n"
		media_manifest_string += "#EXT-X-VERSION:3" + "\n"
		media_manifest_string += "#EXT-X-TARGETDURATION:4" + "\n"
		media_manifest_string += "#EXT-X-MEDIA-SEQUENCE:0" + "\n"
		media_manifest_string += "#EXT-X-PLAYLIST-TYPE:EVENT" + "\n"

		for segment in self.segments[ str(bitrate) ]:
			media_manifest_string += "#EXTINF:" + str(segment.duration)  + "\n" + segment.base_uri + segment.uri + "\n"

		media_manifest_string += "#EXT-X-ENDLIST\n"

		return media_manifest_string
	
	## Returns live master manifest of a given id
	def get_user_master_manifest(self, uid):
		master_manifest_string = ""
		master_manifest_string += "#EXTM3U" + "\n"
		#counter = 0

		for playlist in self.m3u8_obj.playlists:
			master_manifest_string += "#EXT-X-STREAM-INF:" + "AVERAGE-BANDWIDTH="
			master_manifest_string += str(playlist.stream_info.average_bandwidth) + "," + "BANDWIDTH="
			master_manifest_string += str(playlist.stream_info.bandwidth) + "," + "CODECS=" + '"'
			master_manifest_string += playlist.stream_info.codecs + '"'
			#newFileName = str(playlist.stream_info.bandwidth)
			if playlist.stream_info.resolution != None:
				master_manifest_string += ",RESOLUTION="
				resolution = ""
				for res in playlist.stream_info.resolution:
					resolution += str(res)
					master_manifest_string += str(res)
					if res != playlist.stream_info.resolution[-1]:
						master_manifest_string += "x"
						resolution += "x"
			#else:
			master_manifest_string += "\n" + "variant.m3u8?uid="
			master_manifest_string += uid + "&btr=" + str(playlist.stream_info.bandwidth)
			master_manifest_string += "\n"
			#break
			#counter += 1

		return master_manifest_string
