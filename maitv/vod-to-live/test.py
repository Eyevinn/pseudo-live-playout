from vodtolive import HLSVod
import threading

def main():
    
    vod = HLSVod('http://dw2nch8cl472k.cloudfront.net/HLS/Apple%20HLS/HTTP%20example.m3u8')
        #vod.dump()
        #print "LIST PLAYLISTS"
        #vod.list_playlists()
        #print('HLS START')
        playIsActive = True
        
        def timerFunction():
            timer = threading.Timer(3.0, timerFunction)
                if playIsActive == True:
                    timer.start()
                        #print vod.get_segment('18830456')
                        
                        for bw in vod.m3u8_obj.playlists:
                            bandwidths = []
                                bw = bw.stream_info.bandwidth
                                bandwidths.append(bw)
                                #print("Bandwidth")
                                #print bw
                                for x in bandwidths:
                                    print "2 SEGMENTS with bandwidth " + str(x)
                                        #print x
                                        print vod.get_segment(str(x))
                        #print vod.get_segment('18830456')
                    vod.next()
            
                else:
                    timer.cancel()
                        timerFunction()

if __name__ == '__main__':
    try:
        main()
        except Exception, err:
        raise
