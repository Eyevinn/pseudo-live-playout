
import time
from vodtolive import HLSVod

class User:

    session_id_counter = 1

    def __init__(self, user_name):
        self.my_id = User.session_id_counter
        User.session_id_counter += 1
        self.user_name = user_name
        self.tableu = ['http://dw2nch8cl472k.cloudfront.net/HLS/Apple%20HLS/HTTP%20example.m3u8']
        self.tab_index = 0
        self.curret_tab_start = time.mktime(time.gmtime())

    def my_id(self):
        return self.session_id_counter

    def get_name(self)
        return self.user_name

    def restart(self):
        self.curret_tab_start = time.mktime(time.gmtime())

    def request_main(self, uid):
        self.vod = HLSVod(self.tableu[self.tab_index])
        return vod.get_user_master_manifest(uid)

    def request_variant(self, bandwidth):
        mediamanifeststring = vod.get_live_media_manifest(bandwidth)



