
## @package User
#  <b>User</b> keeps track of one user, incluing user-id, name, 
#  tableu, now-playing.
#  
#  Used to request <b>main</b> (master manifest, whole)
#  or to request <b>variant</b> (manifest for specific bitrate, in snippets)
#  Use <b>next()</b> to advance to next snippet.

import time
from random import randrange
from vodtolive import HLSVod

master_tableu = [
	'http://dw2nch8cl472k.cloudfront.net/HLS/Apple%20HLS/HTTP%20example.m3u8',
	'http://dw2nch8cl472k.cloudfront.net/HLS/Apple%20HLS%202/backhoppning.m3u8',
#	'http://dw2nch8cl472k.cloudfront.net/HLS/Apple%20HLS%203/karleken.m3u8',
	'http://dw2nch8cl472k.cloudfront.net/HLS/Apple%20HLS%204/sportskor.m3u8',
	'http://dw2nch8cl472k.cloudfront.net/HLS/Apple%20HLS%205/STWE2017.m3u8' ]

# this is hardcoded for now, will get info from AI later

master_titles = [
	'Springa', 
	'Backhopp', 
#	'K&auml;rleken', 
	'Sportskor', 
	'STWE']

## The <b>User</b> class, the only primary part of the package
class User:

	## class variable, (ie static) to keep track of next session id
	session_id_counter = 1

	## The constructor
	#  @param user_name Name used to create user
	def __init__(self, user_name):
		self.my_id = User.session_id_counter
		User.session_id_counter += 1
		self.user_name = user_name
		self.tableu = []
		self.titles = []
		self.active = 0
		for x in range(0, 3):
			idx = randrange(len(master_tableu))
			self.tableu.append(master_tableu[idx])
			self.titles.append(master_titles[idx])

		self.sequence_number = 0
		self.tab_index = 0
		self.seg_index = 0
		self.curret_tab_start = time.mktime(time.gmtime())
		self.vods = []
		for idx, pl in enumerate(self.tableu):
			hls = HLSVod(pl)
			self.vods.append(hls)
			self.titles[idx] += " : " + str(hls.get_playlength())

	## Get the id for the user
	def my_id(self):
		return self.session_id_counter

	## Get the name for the user
	def get_name(self):
		return self.user_name

	## Get the now-playing user
	def get_active(self):
		return self.active

	## Start over playback, use with care
	def restart(self):
		self.sequence_number = 0
		self.tab_index = 0
		self.seg_index = 0
		self.curret_tab_start = time.mktime(time.gmtime())

	## Request master manifest
	#  will return the whole master manifest, as a string
	#  you only need to call this once per session
	def request_main(self, uid):
		#self.vod = HLSVod(self.tableu[self.tab_index])
		return self.vods[0].get_user_master_manifest(uid)

	## Request variant manifest snippet
	#  This will return as a string a few posts of the manifest
	#  @param bandwidth The bitrate you want manifest for
	def request_variant(self, bandwidth):
		res = ""
		res += self.vods[self.tab_index].get_header_lead(self.sequence_number)
		res += self.vods[self.tab_index].get_segment(bandwidth, self.seg_index)
		if (self.seg_index+1) >= self.vods[self.tab_index].get_segment_count():
			nxt_tab = self.tab_index + 1
			nxt_seg = 0
			if nxt_tab == len(self.tableu):
				res += self.vods[self.tab_index].get_footer_end()
				return res
			res += self.vods[nxt_tab].get_header_seam()
			res += self.vods[nxt_tab].get_segment(bandwidth, nxt_seg)
		else:
			nxt_tab = self.tab_index
			nxt_seg = self.seg_index + 1
			res += self.vods[nxt_tab].get_header_normal()
			res += self.vods[nxt_tab].get_segment(bandwidth, nxt_seg)
		return res

	## Advance to next snippet
	def next(self):
		self.seg_index += 1
		if self.seg_index >= self.vods[self.tab_index].get_segment_count():
			self.tab_index += 1
			self.seg_index = 0
		self.sequence_number += 1
		if self.seg_index >=4:
			self.active = self.tab_index

