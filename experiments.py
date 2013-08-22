from os.path import join
import helpers
import textwrap
import load_data2
import match_chips2 as mc2
import numpy as np
import os
import params
import report_results2
import sys 

def reload_module():
    import imp
    import sys
    imp.reload(sys.modules[__name__])

def param_config1():
    params.__RANK_EQ__ = True

def param_config2():
    params.__RANK_EQ__ = False


db_dir = load_data2.JAGUARS
def run_experiment():
    db_dir = load_data2.DEFAULT
    print(textwrap.dedent('''
    ======================
    Running Experiment on: %r
    ======================''' % db_dir))
    print params.param_string()
    hs = load_data2.HotSpotter(db_dir)
    qcx2_res = mc2.run_matching(hs)
    report_results2.dump_all(hs, qcx2_res)

def oxford_philbin07():
    params.__MATCH_TYPE__        = 'bagofwords'
    params.__BOW_NUM_WORDS__     = [1e4, 2e4, 5e4, 1e6, 1.25e6][3]
    params.__NUM_RERANK__        = [100, 200, 400, 800, 1000][3]
    params.__CHIP_SQRT_AREA__    = None
    params.__BOW_AKMEANS_FLANN_PARAMS__ = dict(algorithm='kdtree',
                                               trees=8, checks=64)
    # I'm not sure if checks parameter is set correctly
    dbdir = load_data2.OXFORD
    hs = load_data2.HotSpotter(dbdir, load_matcher=False)
    # Use the 55 cannonical test cases 
    hs.load_test_train_database_samples_from_file(test_sample_fname='test_sample55.txt')
    # Quick Sanity Checks
    db_sample_cx = hs.database_sample_cx
    tr_sample_cx = hs.train_sample_cx
    te_sample_cx = hs.test_sample_cx
    assert db_sample_cx == tr_sample_cx
    assert len(set(te_sample_cx)) == 55
    print('Database shape: '+str(np.vstack(hs.feats.cx2_desc[db_sample_cx]).shape))
    # Load / Build Vocabulary
    hs.load_matcher()
    # Run the matching
    qcx2_res = mc2.run_matching(hs)
    report_results2.dump_all(hs, qcx2_res, oxford=True)

def oxford_bow():
    params.__MATCH_TYPE__     = 'bagofwords'
    params.__CHIP_SQRT_AREA__ = None
    params.__BOW_NUM_WORDS__  = [1e4, 2e4, 5e4, 1e6, 1.25e6][0]
    dbdir = load_data2.OXFORD
    hs = load_data2.HotSpotter(dbdir)
    qcx2_res = mc2.run_matching(hs)
    report_results2.dump_all(hs, qcx2_res, oxford=True)

def oxford_vsmany():
    params.__MATCH_TYPE__     = 'vsmany'
    params.__CHIP_SQRT_AREA__ = None
    dbdir = load_data2.OXFORD
    hs = load_data2.HotSpotter(dbdir)
    qcx2_res = mc2.run_matching(hs)
    report_results2.dump_all(hs, qcx2_res, oxford=True)
    pass
    
def mothers_vsmany():
    params.__MATCH_TYPE__     = 'vsmany'
    run_experiment()

def mothers_bow():
    params.__MATCH_TYPE__     = 'bagofwords'
    run_experiment()

import load_data2 as ld2
def demo():
    pass
#ld2.DEFAULT


if __name__ == '__main__':
    from multiprocessing import freeze_support
    import load_data2
    freeze_support()

    arg_map = {
        'philbin'       : oxford_philbin07,
        'oxford-bow'    : oxford_bow,
        'oxford-vsmany' : oxford_vsmany,
        'mothers-bow'    : mothers_bow,
        'mothers-vsmany' : mothers_vsmany,
        'default'       : run_experiment }

    print ('Valid arguments are:\n    '+ '\n    '.join(arg_map.keys()))

    has_arg = False
    for argv in sys.argv:
        if argv in arg_map.keys():
            print('Running '+str(argv))
            arg_map[argv]()
            has_arg = True
        elif argv.find('param') > -1:
            param_config1()
            run_experiment

    if not has_arg:
        run_experiment()
