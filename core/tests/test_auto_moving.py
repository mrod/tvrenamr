import os, shutil

from nose.tools import *

#stub urlopen calls
import urlopenmock

from core.core import TvRenamr

class TestAutoMoving(object):
    working = 'tests/data/working'
    auto_move = 'tests/data/auto_move'
    
    def setUp(self):
        files = 'tests/data/files'
        self.tv = TvRenamr(self.working, log_level='critical')
        for fn in os.listdir(files): shutil.copy(os.path.join(files, fn), os.path.join(self.working, fn))
    
    def tearDown(self):
        for fn in os.listdir(self.working): os.remove(os.path.join(self.working,fn))
        for each_tuple in os.walk(self.auto_move):
            for fname in each_tuple[2]:
                os.remove(os.path.join(each_tuple[0],fname))
        for fn in os.listdir(self.auto_move): shutil.rmtree(os.path.join(self.auto_move,fn))
    
    def test_using_auto_move_renames_the_file_correctly(self):
        fn = 'chuck.s1e06.foo.HD.avi'
        credentials = self.tv.extract_episode_details_from_file(fn)
        title = self.tv.retrieve_episode_name(series=credentials['series'], season=credentials['season'], episode=credentials['episode'])
        credentials['series'] = title['series']
        credentials['title'] = title['title']
        path = self.tv.build_path(series=credentials['series'], season=credentials['season'], episode=credentials['episode'], title=credentials['title'], extension=credentials['extension'], auto_move=self.auto_move)
        self.tv.rename(fn, path)
        assert_true(os.path.isfile(os.path.join(self.auto_move+'/Chuck/Season 1', 'Chuck - 106 - Chuck Versus the Sandworm.avi')))
    
    def test_using_auto_move_moves_the_file_to_the_correct_folder(self):
        fn = 'stargate.sg-1.s10e18.xvid.avi'
        credentials = self.tv.extract_episode_details_from_file(fn)
        title = self.tv.retrieve_episode_name(series=credentials['series'], season=credentials['season'], episode=credentials['episode'])
        credentials['series'] = title['series']
        credentials['title'] = title['title']
        path = self.tv.build_path(series=credentials['series'], season=credentials['season'], episode=credentials['episode'], title=credentials['title'], extension=credentials['extension'], auto_move=self.auto_move)
        self.tv.rename(fn, path)
        for fn in os.listdir(self.auto_move):
            if fn == 'Stargate SG-1':
                full_path = fn
                for other in os.listdir(os.path.join(self.auto_move,fn)):
                    if other == 'Season 10':
                        full_path = full_path +'/'+ other +'/'
                        for fn in os.listdir(os.path.join(self.auto_move,full_path)):
                            full_path = full_path + fn
        assert_equal(full_path, 'Stargate SG-1/Season 10/Stargate SG-1 - 1018 - Family Ties.avi')
    
    def test_using_auto_move_returns_the_correct_path_based_on_the_episode(self):
        credentials = self.tv.extract_episode_details_from_file('true.blood.0205.avi')
        title = self.tv.retrieve_episode_name(series=credentials['series'], season=credentials['season'], episode=credentials['episode'])
        credentials['series'] = title['series']
        credentials['title'] = title['title']
        path = self.tv.build_path(series=credentials['series'], season=credentials['season'], episode=credentials['episode'], title=credentials['title'], extension=credentials['extension'], auto_move=self.auto_move)
        assert_equal(path, 'tests/data/auto_move/True Blood/Season 2/True Blood - 205 - Never Let Me Go.avi')
    
    def test_moving_the_leading_the_to_the_end_of_a_show_name_causes_the_series_folder_name_to_follow_suit_when_using_automove(self):
        fn = 'The.Big.Bang.Theory.S03E01.HDTV.XviD-NoTV.avi'
        credentials = self.tv.extract_episode_details_from_file(fn)
        title = self.tv.retrieve_episode_name(series=credentials['series'], season=credentials['season'], episode=credentials['episode'])
        credentials['title'] = title['title']
        credentials['series'] = self.tv.set_position_of_leading_the_to_end_of_show_name(title['series'])
        path = self.tv.build_path(series=credentials['series'], season=credentials['season'], episode=credentials['episode'], title=credentials['title'], extension=credentials['extension'], auto_move=self.auto_move)
        self.tv.rename(fn, path)
        assert_true(os.path.isdir(os.path.join(self.auto_move, 'Big Bang Theory, The/Season 3')))
    