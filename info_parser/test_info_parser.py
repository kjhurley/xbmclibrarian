'''
Created on 14 Aug 2014

@author: khurley
'''
import unittest
import mock
import info_parser.iplayer_info_parser
import tvdb_api # needed to patch

class Test(unittest.TestCase):
    def testBasicParser(self):
        p=info_parser.iplayer_info_parser.IPlayerInfoParser()
        stream="""INFO: File name prefix = Topsy_and_Tim_Series_2_-_13._Emergency_Rescue_b04bsgc6_default                 
available:      Unknown
categories:     Children's,Entertainment & Comedy,Drama
channel:        CBeebies
desc:           Mrs Higley-Pigley's cat, Tiger, is stuck up the tree outside Topsy and Tim's house.   When Dad and Mr Fen fail to rescue the cat because he has climbed too high, the fire brigade come in a fire engine to help.
descmedium:     Live-action children's show. Mrs Higley-Pigley's cat, Tiger, is stuck up the tree outside Topsy and Tim's house.
descshort:      Mrs Higley-Pigley's cat, Tiger, is stuck up the tree outside Topsy and Tim's house.
dir:            /home/khurley
dldate:         2014-08-14
dltime:         10:11:23
duration:       660
durations:      default: 660
episode:        13. Emergency Rescue
episodenum:     13
episodeshort:   Emergency Rescue
expiry:         2014-08-20T16:30:00Z
expiryrel:      in 6 days 7 hours
ext:            EXT
filename:       /home/khurley/Topsy_and_Tim_Series_2_-_13._Emergency_Rescue_b04bsgc6_default.EXT
filepart:       /home/khurley/Topsy_and_Tim_Series_2_-_13._Emergency_Rescue_b04bsgc6_default.partial.EXT
fileprefix:     Topsy_and_Tim_Series_2_-_13._Emergency_Rescue_b04bsgc6_default
firstbcast:     default: 2014-07-23T17:20:00+01:00
firstbcastrel:  default: 21 days 16 hours ago
index:          1168
lastbcast:      default: 2014-07-23T17:20:00+01:00
lastbcastrel:   default: 21 days 16 hours ago
longname:       Topsy and Tim: Series 2
modes:          default: 
modesizes:      default: 
name:           Topsy and Tim: Series 2
nameshort:      Topsy and Tim
pid:            b04bsgc6
player:         http://www.bbc.co.uk/iplayer/episode/b04bsgc6/Topsy_and_Tim_Series_2_Emergency_Rescue/
senum:          s02e13
seriesnum:      2
thumbfile:      /home/khurley/Topsy_and_Tim_Series_2_-_13._Emergency_Rescue_b04bsgc6_default.jpg
thumbnail:      http://www.bbc.co.uk/iplayer/images/episode/b04bsgc6_150_84.jpg
thumbnail1:     http://ichef.bbci.co.uk/programmeimages/p0230r45/b04bsgc6_86_48.jpg
thumbnail2:     http://ichef.bbci.co.uk/programmeimages/p0230r45/b04bsgc6_150_84.jpg
thumbnail3:     http://ichef.bbci.co.uk/programmeimages/p0230r45/b04bsgc6_178_100.jpg
thumbnail4:     http://ichef.bbci.co.uk/programmeimages/p0230r45/b04bsgc6_512_288.jpg
thumbnail5:     http://ichef.bbci.co.uk/programmeimages/p0230r45/b04bsgc6_528_297.jpg
thumbnail6:     http://ichef.bbci.co.uk/programmeimages/p0230r45/b04bsgc6_640_360.jpg
timeadded:      0 days 0 hours ago (1408005598)
title:          Topsy and Tim: Series 2: Emergency Rescue
type:           tv
verpids:        default: b04bsf62
version:        default
versions:       default

1162:   Topsy and Tim: Series 2 - 4. Busy Builders, CBeebies, Children's,Drama,Entertainment & Comedy
,TV, default
^MINFO: File name prefix = Topsy_and_Tim_Series_2_-_4._Busy_Builders_b0499z1g_default                
 

available:      Unknown
categories:     Children's,Entertainment & Comedy,Drama
channel:        CBeebies
desc:           It's noisy outside Topsy and Tim's house. Their neighbour Mr Fen is building a new driveway and lots of bricks are being delivered. The twins are excited when Mr Fen asks them to help.
descmedium:     Live-action children's show. Topsy and Tim's neighbour Mr Fen is building a new drive
way. Lots of bricks are being delivered, so Mr Fen asks the twins for help.
descshort:      Topsy and Tim's neighbour Mr Fen is building a new driveway.
dir:            /home/khurley
dldate:         2014-08-14
dltime:         10:10:22
duration:       600
durations:      default: 600
episode:        4. Busy Builders
episodenum:     4
episodeshort:   Busy Builders
expiry:         2014-08-16T16:35:00Z
expiryrel:      in 2 days 7 hours
ext:            EXT
filename:       /home/khurley/Topsy_and_Tim_Series_2_-_4._Busy_Builders_b0499z1g_default.EXT
filepart:       /home/khurley/Topsy_and_Tim_Series_2_-_4._Busy_Builders_b0499z1g_default.partial.EXT
fileprefix:     Topsy_and_Tim_Series_2_-_4._Busy_Builders_b0499z1g_default
firstbcast:     default: 2014-07-10T17:20:00+01:00
firstbcastrel:  default: 34 days 16 hours ago
index:          1162
lastbcast:      default: 2014-07-10T17:20:00+01:00
lastbcastrel:   default: 34 days 16 hours ago
longname:       Topsy and Tim: Series 2
modes:          default: 
modesizes:      default: 
name:           Topsy and Tim: Series 2
nameshort:      Topsy and Tim
pid:            b0499z1g
player:         http://www.bbc.co.uk/iplayer/episode/b0499z1g/Topsy_and_Tim_Series_2_Busy_Builders/
senum:          s02e04
seriesnum:      2
thumbfile:      /home/khurley/Topsy_and_Tim_Series_2_-_4._Busy_Builders_b0499z1g_default.jpg
thumbnail:      http://www.bbc.co.uk/iplayer/images/episode/b0499z1g_150_84.jpg
thumbnail1:     http://ichef.bbci.co.uk/programmeimages/p0222k11/b0499z1g_86_48.jpg
thumbnail2:     http://ichef.bbci.co.uk/programmeimages/p0222k11/b0499z1g_150_84.jpg
thumbnail3:     http://ichef.bbci.co.uk/programmeimages/p0222k11/b0499z1g_178_100.jpg
thumbnail4:     http://ichef.bbci.co.uk/programmeimages/p0222k11/b0499z1g_512_288.jpg
thumbnail5:     http://ichef.bbci.co.uk/programmeimages/p0222k11/b0499z1g_528_297.jpg
thumbnail6:     http://ichef.bbci.co.uk/programmeimages/p0222k11/b0499z1g_640_360.jpg
timeadded:      0 days 0 hours ago (1408005598)
title:          Topsy and Tim: Series 2: Busy Builders
type:           tv
verpids:        default: b0499z16
version:        default
versions:       default
web:            http://www.bbc.co.uk/programmes/b0499z1g.html

"""
        p.parse(stream.splitlines())
        self.assertEqual(len(p.shows),2)
        self.assertEqual(str(p.shows[0]),"Topsy and Tim;Emergency Rescue;s02.e13 [tvdb=None]")
        self.assertEqual(p.shows[0].show_name,"Topsy and Tim")
        self.assertEqual(p.shows[0].episode_title,"Emergency Rescue")
        self.assertEqual(str(p.shows[1]),"Topsy and Tim;Busy Builders;s02.e04 [tvdb=None]")
        self.assertEqual(p.shows[1].show_name,"Topsy and Tim")
        self.assertEqual(p.shows[1].episode_title,"Busy Builders")
        self.assertEqual(p.shows[1].episode_number,(2,4))

    def test_horizon(self):
        info_stream="""INFO: File name prefix = Horizon_-_2010-2011_10._Science_Under_Attack_b00y4yql_default                 

available:      Unknown
categories:     Factual,Science & Nature
channel:        BBC Web Only
desc:           Nobel Prize winner Sir Paul Nurse examines why science appears to be under attack, and why public trust in key scientific theories has been eroded - from the theory that man-made climate change is warming our planet, to the safety of GM food, or that HIV causes AIDS.   He interviews scientists and campaigners from both sides of the climate change debate, and travels to New York to meet Tony, who has HIV but doesn't believe that that the virus is responsible for AIDS.  This is a passionate defence of the importance of scientific evidence and the power of experiment, and a look at what scientists themselves need to do to earn trust in controversial areas of science in the 21st century.
descmedium:     Nobel Prize winner Sir Paul Nurse examines why science appears to be under attack, and why public trust in key scientific theories has been eroded.
descshort:      Nobel Prize winner Sir Paul Nurse examines why science appears to be under attack.
dir:            /home/khurley
dldate:         2014-08-14
dltime:         12:14:26
duration:       3540
durations:      default: 3540
episode:        2010-2011: 10. Science Under Attack
episodenum:     10
episodeshort:   2010-2011: Science Under Attack
expiry:         2099-01-01T00:00:00Z
expiryrel:      in 84 years 139 days 12 hours
ext:            EXT
filename:       /home/khurley/Horizon_-_2010-2011_10._Science_Under_Attack_b00y4yql_default.EXT
filepart:       /home/khurley/Horizon_-_2010-2011_10._Science_Under_Attack_b00y4yql_default.partial.EXT
fileprefix:     Horizon_-_2010-2011_10._Science_Under_Attack_b00y4yql_default
firstbcast:     default: 2014-05-20T10:00:00+01:00
firstbcastrel:  default: 86 days 2 hours ago
index:          490
lastbcast:      default: 2014-05-20T10:00:00+01:00
lastbcastrel:   default: 86 days 2 hours ago
longname:       Horizon
modes:          default: 
modesizes:      default: 
name:           Horizon
nameshort:      Horizon
pid:            b00y4yql
player:         http://www.bbc.co.uk/iplayer/episode/b00y4yql/Horizon_20102011_Science_Under_Attack/
senum:          s00e10
thumbfile:      /home/khurley/Horizon_-_2010-2011_10._Science_Under_Attack_b00y4yql_default.jpg
thumbnail:      http://www.bbc.co.uk/iplayer/images/episode/b00y4yql_150_84.jpg
thumbnail1:     http://ichef.bbci.co.uk/programmeimages/p01gzrsm/b00y4yql_86_48.jpg
thumbnail2:     http://ichef.bbci.co.uk/programmeimages/p01gzrsm/b00y4yql_150_84.jpg
thumbnail3:     http://ichef.bbci.co.uk/programmeimages/p01gzrsm/b00y4yql_178_100.jpg
thumbnail4:     http://ichef.bbci.co.uk/programmeimages/p01gzrsm/b00y4yql_512_288.jpg
thumbnail5:     http://ichef.bbci.co.uk/programmeimages/p01gzrsm/b00y4yql_528_297.jpg
thumbnail6:     http://ichef.bbci.co.uk/programmeimages/p01gzrsm/b00y4yql_640_360.jpg
timeadded:      0 days 2 hours ago (1408005598)
title:          Horizon: 2010-2011: Science Under Attack
type:           tv
verpids:        default: p01z2k3m
version:        default
versions:       default
web:            http://www.bbc.co.uk/programmes/b00y4yql.html
"""
        p=info_parser.iplayer_info_parser.IPlayerInfoParser()
        p.parse(info_stream.splitlines())
    
        self.assertEqual(str(p.shows[0]),"Horizon;Science Under Attack;s00.e10 [tvdb=None]")
        
        #with mock.patch("tvdb_api.Tvdb.__getitem__") as tv:
        #    p.shows[0].cross_check_with_tvdb()
        #    print tv.called


    def test_dragons_riders(self):
        info_stream="""available:      Unknown
categories:     Children's,Animation
channel:        CBBC
desc:           Animation based on How to Train Your Dragon. Mildew helped Alvin kidnapping Hiccup an
d Toothless by forging Bork's night fury notes. However, Mildew is imprisoned himself when he is no l
onger of any use to Alvin. Hiccup reluctantly allows Mildew to help him find Toothless and escape Out
cast Island. It is a final test for Mildew's loyalty to Berk.
descmedium:     Animation based on How to Train Your Dragon. Mildew helps Hiccup to find Toothless an
d escape Outcast Island. It is a final test for Mildew's loyalty to Berk.
descshort:      Mildew helps Hiccup to find Toothless and escape Outcast Island.
dir:            /home/khurley/src/tvdb_api
dldate:         2014-08-14
dltime:         13:52:43
duration:       1260
durations:      default: 1260
episode:        We Are Family Part 2
episodeshort:   We Are Family Part 2
expiry:         2014-08-15T14:35:00Z
expiryrel:      in 1 days 1 hours
ext:            EXT
filename:       /home/khurley/src/tvdb_api/Dragons_-_Riders_of_Berk_Series_1_-_We_Are_Family_Part_2_b
03h79yk_default.EXT
        filepart:       /home/khurley/src/tvdb_api/Dragons_-_Riders_of_Berk_Series_1_-_We_Are_Family_Part_2_b
03h79yk_default.partial.EXT
fileprefix:     Dragons_-_Riders_of_Berk_Series_1_-_We_Are_Family_Part_2_b03h79yk_default
firstbcast:     default: 2014-07-18T17:00:00+01:00
firstbcastrel:  default: 26 days 20 hours ago
index:          334
lastbcast:      default: 2014-07-18T17:00:00+01:00
lastbcastrel:   default: 26 days 20 hours ago
longname:       Dragons - Riders of Berk: Series 1
modes:          default: 
modesizes:      default: 
name:           Dragons - Riders of Berk: Series 1
nameshort:      Dragons - Riders of Berk
pid:            b03h79yk
player:         http://www.bbc.co.uk/iplayer/episode/b03h79yk/Dragons_Riders_of_Berk_Series_1_We_Are_
Family_Part_2/
senum:          s01e00
seriesnum:      1
thumbfile:      /home/khurley/src/tvdb_api/Dragons_-_Riders_of_Berk_Series_1_-_We_Are_Family_Part_2_b
03h79yk_default.jpg
thumbnail:      http://www.bbc.co.uk/iplayer/images/episode/b03h79yk_150_84.jpg
thumbnail1:     http://ichef.bbci.co.uk/programmeimages/p022nmln/b03h79yk_86_48.jpg
thumbnail2:     http://ichef.bbci.co.uk/programmeimages/p022nmln/b03h79yk_150_84.jpg
thumbnail3:     http://ichef.bbci.co.uk/programmeimages/p022nmln/b03h79yk_178_100.jpg
thumbnail4:     http://ichef.bbci.co.uk/programmeimages/p022nmln/b03h79yk_512_288.jpg
thumbnail5:     http://ichef.bbci.co.uk/programmeimages/p022nmln/b03h79yk_528_297.jpg
thumbnail6:     http://ichef.bbci.co.uk/programmeimages/p022nmln/b03h79yk_640_360.jpg
timeadded:      0 days 4 hours ago (1408005598)
title:          Dragons - Riders of Berk: Series 1: We Are Family Part 2
type:           tv
verpids:        default: b03bshvw
version:        default
versions:       default
web:            http://www.bbc.co.uk/programmes/b03h79yk.html
        """ 
        p=info_parser.iplayer_info_parser.IPlayerInfoParser()
        p.parse(info_stream.splitlines())
    
        self.assertEqual(str(p.shows[0]),"Dragons;We Are Family (2);s01.e00 [tvdb=None]")


    def test_bakeoff_extra_slice(self):
        info_stream="""1037:   The Great British Bake Off - An Extra Slice: Episode 1, BBC Two, Food & Drink,Lifestyle & Leisure,Popular,TV, default,
^MINFO: File name prefix = The_Great_British_Bake_Off_-_An_Extra_Slice_Episode_1_b04dclt8_default                 

available:      Unknown
categories:     Lifestyle & Leisure,Food & Drink
channel:        BBC Two
desc:           The Bake Off is back...and this year it is joined by An Extra Slice of Bake Off magic in this sister show for BBC Two.  Each week, host Jo Brand is joined by three different celebrity Bake Off fans. Jo shines a spotlight on the good, the bad and the soggy bottomed from the week's episode with chat, unseen footage from the BBC One show and an interview with the week's eliminated baker.  The studio audience are challenged to bring a bake in from home from the week's baking theme, be that bread, pastry, or cakes, and viewers are invited to share photos of their efforts too.  Kicking off the series, Jo and her panel of Bake Off fans will discuss the 12 new bakers and their bakes. The theme this week is cakes. What do the panel think of the bakers' Swiss roll? And how did they fare with their first ever technical challenge - Mary Berry's cherry cake? Whose 36 miniature cakes stopped the show? Plus lots of 'exclusive' footage from the tent.  An Extra Slice... when one helping of Bake Off just isn't enough.
descmedium:     Jo Brand is joined by three celebrity Great British Bake Off fans to take a look at the week's episode, with chat, unseen footage and an interview with the eliminated baker.
descshort:      Jo and her panel of Bake Off fans discuss the 12 new bakers and their bakes.
dir:            /home/khurley
dldate:         2014-08-14
dltime:         14:43:25
duration:       1800
durations:      default: 1800
episode:        An Extra Slice: Episode 1
episodenum:     1
episodeshort:   An Extra Slice
expiry:         2014-10-17T20:29:00Z
expiryrel:      in 64 days 6 hours
ext:            EXT
filename:       /home/khurley/The_Great_British_Bake_Off_-_An_Extra_Slice_Episode_1_b04dclt8_default.EXT
filepart:       /home/khurley/The_Great_British_Bake_Off_-_An_Extra_Slice_Episode_1_b04dclt8_default.partial.EXT
fileprefix:     The_Great_British_Bake_Off_-_An_Extra_Slice_Episode_1_b04dclt8_default
firstbcast:     default: 2014-08-08T21:00:00+01:00
firstbcastrel:  default: 5 days 17 hours ago
index:          1037
lastbcast:      default: 2014-08-08T21:00:00+01:00
lastbcastrel:   default: 5 days 17 hours ago
longname:       The Great British Bake Off
modes:          default: 
modesizes:      default: 
name:           The Great British Bake Off
nameshort:      The Great British Bake Off
pid:            b04dclt8
player:         http://www.bbc.co.uk/iplayer/episode/b04dclt8/The_Great_British_Bake_Off_An_Extra_Slice_Episode_1/
senum:          s00e01
thumbfile:      /home/khurley/The_Great_British_Bake_Off_-_An_Extra_Slice_Episode_1_b04dclt8_default.jpg
thumbnail:      http://www.bbc.co.uk/iplayer/images/episode/b04dclt8_150_84.jpg
thumbnail1:     http://ichef.bbci.co.uk/programmeimages/p024rncy/b04dclt8_86_48.jpg
thumbnail2:     http://ichef.bbci.co.uk/programmeimages/p024rncy/b04dclt8_150_84.jpg
thumbnail3:     http://ichef.bbci.co.uk/programmeimages/p024rncy/b04dclt8_178_100.jpg
thumbnail4:     http://ichef.bbci.co.uk/programmeimages/p024rncy/b04dclt8_512_288.jpg
thumbnail5:     http://ichef.bbci.co.uk/programmeimages/p024rncy/b04dclt8_528_297.jpg
thumbnail6:     http://ichef.bbci.co.uk/programmeimages/p024rncy/b04dclt8_640_360.jpg
timeadded:      0 days 5 hours ago (1408005598)
title:          The Great British Bake Off: An Extra Slice: Episode 1
type:           tv
verpids:        default: b04dclt5
version:        default
versions:       default
web:            http://www.bbc.co.uk/programmes/b04dclt8.html

        """ 
        p=info_parser.iplayer_info_parser.IPlayerInfoParser()
        p.parse(info_stream.splitlines())
    
        self.assertEqual(str(p.shows[0]),"The Great British Bake Off: An Extra Slice;Episode 1;s00.e01 [tvdb=None]")

    def test_sky_at_night(self):
        info_stream="""1107:   The Sky at Night - How to Catch a Comet, BBC Four, Factual,Science & Nature,TV, default
^MINFO: File name prefix = The_Sky_at_Night_-_How_to_Catch_a_Comet_b04dg5jq_default                 

available:      Unknown
categories:     Factual,Science & Nature
channel:        BBC Four
desc:           The team goes behind the scenes at mission control for the critical point of the most ambitious space project of the decade. The European Space Agency's Rosetta probe finally catches up with the comet it has been chasing across the solar system for ten years and prepares to send out a lander armed with drills and harpoons for a daredevil attempt to hitch a ride.   With the latest images revealing that it may even be two comets stuck together, Dr Chris Lintott is on hand in Germany with updates from the mission team on this unparalleled challenge, whilst Dr Maggie Aderin- Pocock reveals the instruments that the lander is carrying.
descmedium:     The team is at mission control as the Rosetta probe catches up with the comet it has been chasing across the solar system and prepares to send out a lander.
descshort:      The Rosetta probe catches up with the comet it has been chasing across the solar system.
dir:            /home/khurley/src/tvdb_api
dldate:         2014-08-14
dltime:         15:34:03
duration:       1800
durations:      default: 1800
episode:        How to Catch a Comet
episodeshort:   How to Catch a Comet
expiry:         2014-08-21T00:30:00Z
expiryrel:      in 6 days 9 hours
ext:            EXT
filename:       /home/khurley/src/tvdb_api/The_Sky_at_Night_-_How_to_Catch_a_Comet_b04dg5jq_default.EXT
filepart:       /home/khurley/src/tvdb_api/The_Sky_at_Night_-_How_to_Catch_a_Comet_b04dg5jq_default.partial.EXT
fileprefix:     The_Sky_at_Night_-_How_to_Catch_a_Comet_b04dg5jq_default
firstbcast:     default: 2014-08-10T23:00:00+01:00
firstbcastrel:  default: 3 days 16 hours ago
index:          1107
lastbcast:      default: 2014-08-10T23:00:00+01:00
lastbcastrel:   default: 3 days 16 hours ago
longname:       The Sky at Night
modes:          default: 
modesizes:      default: 
name:           The Sky at Night
nameshort:      The Sky at Night
pid:            b04dg5jq
player:         http://www.bbc.co.uk/iplayer/episode/b04dg5jq/The_Sky_at_Night_How_to_Catch_a_Comet/
thumbfile:      /home/khurley/src/tvdb_api/The_Sky_at_Night_-_How_to_Catch_a_Comet_b04dg5jq_default.jpg
thumbnail:      http://www.bbc.co.uk/iplayer/images/episode/b04dg5jq_150_84.jpg
thumbnail1:     http://ichef.bbci.co.uk/programmeimages/p024fk4h/b04dg5jq_86_48.jpg
thumbnail2:     http://ichef.bbci.co.uk/programmeimages/p024fk4h/b04dg5jq_150_84.jpg
thumbnail3:     http://ichef.bbci.co.uk/programmeimages/p024fk4h/b04dg5jq_178_100.jpg
thumbnail4:     http://ichef.bbci.co.uk/programmeimages/p024fk4h/b04dg5jq_512_288.jpg
thumbnail5:     http://ichef.bbci.co.uk/programmeimages/p024fk4h/b04dg5jq_528_297.jpg
thumbnail6:     http://ichef.bbci.co.uk/programmeimages/p024fk4h/b04dg5jq_640_360.jpg
timeadded:      0 days 5 hours ago (1408005598)
title:          The Sky at Night: How to Catch a Comet
type:           tv
verpids:        default: b04dg5jn
version:        default
versions:       default
web:            http://www.bbc.co.uk/programmes/b04dg5jq.html

        """ 
        p=info_parser.iplayer_info_parser.IPlayerInfoParser()
        p.parse(info_stream.splitlines())
    
        self.assertEqual(str(p.shows[0]),"The Sky at Night;How to Catch a Comet;s00.e00 [tvdb=None]")

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testBasicParser']
    unittest.main()