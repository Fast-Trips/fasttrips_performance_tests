USAGE = r"""
    Iterates through a set of performance tests based on set number it is give.
    
    python performance_tests.py <setnum> <base_directory> [ --norun ]
    
    Base directory is where folders with each of the test run inputs is.
    
    --norun flag can be used to make sure you are iterating thru all the right things before setting up a zillion runs.
    
    e.g. python performance_tests.py set1 ''
    """

levels = {
    "low": {
        "disp"          : 0.2,
        "transfer_fare_ignore_pathfinding"  : True,
        "transfer_fare_ignore_pathenum"     : True,      
        "overlap"       :'None',
        "overlap_split" : False,
        "max_revisit"   : 1,
        "dt"            : 15,
        },
    "high": {
        "disp"          : 0.9,
        "transfer_fare_ignore_pathfinding"  : False,
        "transfer_fare_ignore_pathenum"     : False,
        "overlap"         : 'distance',
        "overlap_split"   : True,
        "max_revisit"     : 5,
        "dt"              : 30,
        },
    }

test_sets = {
    "set1": {
        "processors" : [10, 5, 1],
        "inputs"     : ["Richmond_144",
                      "SF_144",
                      "SM_144",
                      "Bay_144",
                      "SF_1440",
                      "SM_1440",
                      "Richmond_1440",
                      "Bay_1440"],
        "levels" : ["low", "high"] },
    "set2": {
        "processors" : [10, 5, 1],
        "inputs"     : ["Richmond_14400"],
        "levels" : ["low", "high"] },
    "set3": {
        "processors" : [10, 5, 1],
        "inputs"     : ["SF_14400"],
        "levels" : ["low", "high"] },
    "set4": {
        "processors" : [10, 5, 1],
        "inputs"     : ["SM_14400"],
        "levels" : ["low", "high"] },
    "set5": {
        "processors" : [10, 5, 1],
        "inputs"     : ["SM_14400"],
        "levels" : ["low", "high"] },
    }






if __name__ == "__main__":
    import os, itertools, argparse

    parser = argparse.ArgumentParser(description=USAGE)
    parser.add_argument('set_num', type=str, help="Performance Test Number: set1...set5", choices=["set1","set2","set3","set4","set5"])
    parser.add_argument('base_dir', type=str, help="Base Directory")
    parser.add_argument('--norun', help="don't actually run Fast-Trips", action="store_true")
    args    = parser.parse_args()
    set_num = args.set_num
    base_dir= args.base_dir
    run_count = 0
    
    for proc, inp, lev in itertools.product(test_sets[set_num]["processors"],
                                            test_sets[set_num]["inputs"],
                                            test_sets[set_num]["levels"]):
    
        run_config     = os.path.join(base_dir,"config_ft.txt") 
        pathweights    = os.path.join(base_dir,"pathweights_ft.txt") 
        network_inputs = os.path.join(base_dir,"network")
        demand_inputs  = os.path.join(base_dir,inp)
        output_folder  = "out%s_%s_%s" % (inp,proc,lev)
        
        run_count += 1
    
        if args.norun:
            print "RUN SETTINGS"
            print "Processors: %d" % (proc)
            print "Demand Input Dir:  %s" % (demand_inputs)
            print "Level Settings:\n", levels[lev]
            print "Input Level: %s" % (inp)
            print "out folder %s\n" % (output_folder)
        
        else:
            if os.path.exists(output_folder):
                print "Path exists [%s] -- skipping" % output_folder
            else:
                from fasttrips import Run
                Run.run_fasttrips(input_network_dir= network_inputs,
                                  input_demand_dir = demand_inputs,
                                  run_config       = run_config,
                                  input_weights    = pathweights,
                                  output_dir       = base_dir,
                                  iters            = 1,
                                  output_folder    = output_folder,
                                  number_of_processes    = proc,
                                  dispersion             = levels[lev]["disp"],
                                  overlap_split_transit  = levels[lev]["overlap_split"],
                                  overlap_variable       = levels[lev]["overlap"],
                                  max_stop_process_count = levels[lev]["max_revisit"],
                                  time_window            = levels[lev]["dt"],
                                  transfer_fare_ignore_pathfinding = levels[lev]["transfer_fare_ignore_pathfinding"],
                                  transfer_fare_ignore_pathenum = levels[lev]["transfer_fare_ignore_pathenum"], 
                                  )

    if args.norun:
        print "TOTAL RUNS: %d" % (run_count)
