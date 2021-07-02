import pstats
import sys

p = pstats.Stats(sys.argv[1])

p.print_stats()
