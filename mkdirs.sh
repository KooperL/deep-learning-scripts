#!/bin/bash

# touch?

#cd '/media/kooper/HDD/Team Fortress 2'
cd '/media/kooper/HDD/Call of Duty  Modern Warfare 2019'
game="cod_mw"


mkdir datasets
mkdir datasets/$game

cat1=("images" "labels")
cat2=("test" "train" "val")

for item1 in "${cat1[@]}"
do
mkdir -p datasets/$game/$item1
touch "$item1"
for item2 in "${cat2[@]}"
do
mkdir -p datasets/$game/$item1/$item2
touch "$item2"
done
done

# mkdir datasets/$game/images/train
# mkdir datasets/$game/images/val

# mkdir datasets/$game/labels
# mkdir datasets/$game/labels/test
# mkdir datasets/$game/labels/train
# mkdir datasets/$game/labels/val
