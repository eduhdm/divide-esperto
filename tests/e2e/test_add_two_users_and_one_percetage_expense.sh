#!/bin/bash

# To run these tests, run export PYTHONPATH="/path/to/root/folder"

TEST=$(cat << EOF | python src/main.py
adduser Lucas
adduser Eduardo
addexpense
percentage
100
First expense
1
1 2
20 80
get_user_balance 1
EOF
)

EXPECTED_OUTPUT='You are owed 80.0'

if [[ "$TEST" == *"$EXPECTED_OUTPUT"* ]]; then
    echo "Output is correct"
else
    echo "Output is incorrect"
    exit 1
fi

TEST2=$(cat << EOF | python src/main.py
adduser Lucas
adduser Eduardo
addexpense
percentage
100
First expense
1
1 2
20 80
get_user_balance 2
EOF
)

EXPECTED_OUTPUT2='You owe 80.0'

if [[ "$TEST2" == *"$EXPECTED_OUTPUT2"* ]]; then
    echo "Output is correct"
else
    echo "Output is incorrect"
    exit 1
fi


exit 0
