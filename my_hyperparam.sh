#!/usr/bin/bash

POWER_MULT=(0.1 0.4 0.7 1)
THERM_MULT=(0.1 0.4 0.7 1)
VIS_MULT=(0.1 0.4 0.7 1)

# Added extra values

daylighting=("True" "False")
season=("heating" "cooling")
blinds=("False" "True")
control_blinds_multi=("False" "True")

# number of runs (small (4) for testing and larg (400) for getting results)
end_run=1


occupancy=True
agent=PPO
network=leaky
#POWER_MULT=(0.1)
#THERM_MULT=(0.1)
#VIS_MULT=(0.1)

for power_mult in ${POWER_MULT[@]} ; do
  for therm_mult in ${THERM_MULT[@]} ; do
    for vis_mult in ${VIS_MULT[@]} ; do
      for d in "${daylighting[@]}"; do
        for s in "${season[@]}"; do
          for b in "${blinds[@]}"; do
            for c in "${control_blinds_multi[@]}"; do
              ARGS="--daylighting $d --season $s --blinds $b --control_blinds_multi $c"
              export power_mult therm_mult vis_mult occupancy agent network ARGS end_run
              ./my_hyperparam_ppo.sh
       		#      sbatch hyperparam_dueling.sh
	        #       sbatch hyperparam_dqn_one_run.sh
            done
          done
        done
      done
    done
  done
done
