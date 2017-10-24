
import time
from vodtolive import HLSVod

class User:

	session_id_counter = 1

	def __init__(self, user_name):
		self.my_id = User.session_id_counter
		User.session_id_counter += 1
		self.user_name = user_name
		self.tableu = [
			'http://dw2nch8cl472k.cloudfront.net/HLS/Apple%20HLS/HTTP%20example.m3u8',
			'http://dw2nch8cl472k.cloudfront.net/HLS/Apple%20HLS/HTTP%20example.m3u8']
		self.tab_index = 0
		self.seg_index = 0
		self.curret_tab_start = time.mktime(time.gmtime())
		self.vods = []
		for pl in self.tableu:
			self.vods.append(HLSVod(self.tableu[self.tab_index]))
			print "added one playlist"


	def my_id(self):
		return self.session_id_counter

	def get_name(self):
		return self.user_name

	def restart(self):
		self.curret_tab_start = time.mktime(time.gmtime())


	def request_main(self, uid):
		#self.vod = HLSVod(self.tableu[self.tab_index])
		return self.vods[0].get_user_master_manifest(uid)

	def request_variant(self, bandwidth):
		#print "trying to get bandwidth " + str(bandwidth)
		#print self.vod.list_bitrates()
		res = ""
		res += self.vods[self.tab_index].get_header_lead(self.seg_index)
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

	def next(self):
		self.seg_index += 1
		if self.seg_index >= self.vods[self.tab_index].get_segment_count():
			self.tab_index += 1
			self.seg_index = 0


