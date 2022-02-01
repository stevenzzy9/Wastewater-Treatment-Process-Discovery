import os
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.inductive import algorithm as inductive_miner

log = xes_importer.apply(os.path.join("log1.xes"))

net, initial_marking, final_marking = inductive_miner.apply(log)

from pm4py.algo.conformance.alignments import algorithm as alignments
alignments = alignments.apply_log(log, net, initial_marking, final_marking)
