This computes for each kanton the pollution that its citizens are on average exposed to.
(That is: Pollution values are not averaged across space but across citizens,
assuming that each citizen spends 100% of their time at the village/city they are registered at.)


Execute the following command:
bin/do-all.sh


The results will be written to the following file:
results/pollution-by-kanton.txt       (human-readable)
results/pollution-by-kanton.json      (machine-readable, used by the python webapp)


