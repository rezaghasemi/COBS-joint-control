#!/bin/bash

echo "prog started at: `date`"


python3 main.py $ARGS --random_occupancy $occupancy --vav False --multi_agent False --network $network --control_sat True --load_sat False --load_sat_path '<REMOVED>' --control_therm False --power_mult $power_mult --therm_mult $therm_mult --vis_mult $vis_mult --save_root '/media/reza/Tempo/github/Individ study/Codes/COBS-joint-control/rl_results' --end_run $end_run --agent_type $agent --reward_type OCTO --eplus_path '/usr/local/EnergyPlus-9-3-0/'
