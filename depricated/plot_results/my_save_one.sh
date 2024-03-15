#!/bin/bash


echo "prog started at: `date`"

python3 my_save.py --rp1 $power_mult --rp2 $therm_mult --rp3 $vis_mult --a $agent --b $blinds --d $dlights --s $season
