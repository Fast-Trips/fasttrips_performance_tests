USAGE =r"""

  Iterates through performance runs in the current directory -- e.g. all subdirs starting with 'out'.

  Copies ft_output_performance.csv, ft_output_performance_pathfinding.csv, and ft_output_config.txt
  to the given destination directory, prepended by the output directory.

"""

COPYFILES = [
    "ft_output_performance.csv",
    "ft_output_performance_pathfinding.csv",
    "ft_output_config.txt"]

if __name__ == "__main__":
    import os, argparse, shutil, sys

    parser = argparse.ArgumentParser(description=USAGE)
    parser.add_argument('dest_dir', type=str, help="Destination directory")

    args    = parser.parse_args()

    # verify destination directory makes sense
    print "Using destination directory %s" % args.dest_dir
    if not os.path.exists(args.dest_dir):
        print " == doesn't exist.  Aborting"
        sys.exit(2)
    if not os.path.isdir(args.dest_dir):
        print " == is not a directory.  Aborting"
        sys.exit(2)

    for perfdir in os.listdir("."):
        # only care about directories
        if not os.path.isdir(perfdir):
            continue
        # that start with out
        if not perfdir.startswith("out"):
            continue

        for filename in COPYFILES:
            src_file  = os.path.join(perfdir, filename)
            dest_file = os.path.join(args.dest_dir, "%s_%s" % (perfdir, filename[10:]))

            if os.path.exists(dest_file):
                print "Skipping copying to %s" % dest_file
            else:
                shutil.copy2(src_file, dest_file)
                print "Copied %-60s to %s" % (src_file, dest_file)

    print "Completed"

