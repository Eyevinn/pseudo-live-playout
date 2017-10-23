import m3u8
import os

def folderof(s):
    return os.path.dirname(s) + "/"

class HLSVod:
    def __init__(self, hlsManifestUri):
        self.hlsManifestUri = hlsManifestUri
        self.m3u8_obj = m3u8.load(self.hlsManifestUri)
        self.segments = {}
        self.uris = {}

        for playlist in self.m3u8_obj.playlists:
            pth = self.m3u8_obj.base_uri + playlist.uri
            m3u8_playlist = m3u8.load(pth)
            for segment in m3u8_playlist.segments:
                key = str(playlist.stream_info.bandwidth)
                if not key in self.segments:
                    self.uris[key] = folderof(pth)
                    self.segments[key] = []
                self.segments[key].append(segment)
        self.index = 0

    def list_playlists(self):
        print self.m3u8_obj.playlists

    def list_bitrates(self):
        res = ""
        for btr in self.segments:
            res += str(btr) + ", "
        return res
    
    def next(self):
        self.index += 1
    
    def get_segment(self, bitrate):

        #print "--- GET SEGMENT ---"
        #print str(bitrate)
        #print self.uris[bitrate]

        res = ""

        res += "#EXTM3U" + "\n"
        res += "#EXT-X-VERSION:3" + "\n"
        res += "#EXT-X-TARGETDURATION:4" + "\n"
        res += "#EXT-X-MEDIA-SEQUENCE:" + str(self.index) + "\n"
        #res += "#EXT-X-PLAYLIST-TYPE:EVENT" + "\n"
        res += "#EXTINF:" + str(self.segments[bitrate][self.index].duration)  + "\n"
        res += self.uris[bitrate] + self.segments[bitrate] [self.index].uri    + "\n"
        res += "#EXTINF:" + str(self.segments[bitrate][self.index+1].duration)  + "\n"
        res += self.uris[bitrate] + self.segments[bitrate] [self.index+1].uri  + "\n"
            
        return res

    def dump(self):
        print self.segments

    def get_live_master_manifest(self):
        master_manifest_string = ""
        master_manifest_string += "#EXTM3U" + "\n"
        counter = 0

        for playlist in self.m3u8_obj.playlists:
            master_manifest_string += "#EXT-X-STREAM-INF:" + "AVERAGE-BANDWIDTH=" + str(playlist.stream_info.average_bandwidth) + "," + "BANDWIDTH=" + str(playlist.stream_info.bandwidth) + "," + "CODECS=" + '"' + playlist.stream_info.codecs + '"'
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

    def get_live_media_manifest(self, bitrate):
        media_manifest_string = ""
        media_manifest_string += "#EXTM3U" + "\n"
        media_manifest_string += "#EXT-X-VERSION:3" + "\n"
        media_manifest_string += "#EXT-X-TARGETDURATION:4" + "\n"
        media_manifest_string += "#EXT-X-MEDIA-SEQUENCE:0" + "\n"
        media_manifest_string += "#EXT-X-PLAYLIST-TYPE:EVENT" + "\n"

        for segment in self.segments[ str(bitrate) ]:
            media_manifest_string += "#EXTINF:" + str(segment.duration)  + "\n" + segment.base_uri + segment.uri + "\n"

        return media_manifest_string
    
    def get_user_master_manifest(self, uid):
        master_manifest_string = ""
        master_manifest_string += "#EXTM3U" + "\n"
        #counter = 0

        for playlist in self.m3u8_obj.playlists:
            master_manifest_string += "#EXT-X-STREAM-INF:" + "AVERAGE-BANDWIDTH=" + str(playlist.stream_info.average_bandwidth) + "," + "BANDWIDTH=" + str(playlist.stream_info.bandwidth) + "," + "CODECS=" + '"' + playlist.stream_info.codecs + '"'
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
            #    newFileName = "audio"
            master_manifest_string += "\n" + "variant.m3u8?uid="
            master_manifest_string += uid + "&btr=" + str(playlist.stream_info.bandwidth)
            master_manifest_string += "\n"

            #counter += 1

        return master_manifest_string
