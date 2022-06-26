#!/bin/bash

TEST=$(cat << EOF | dividexp
adduser Lucas
adduser Eduardo
addexpense
equal
100
First expense
1
1 2
get_user_balance 1
EOF
)

EXPECTED_OUTPUT='You are owed 50.0'

if [[ "$TEST" == *"$EXPECTED_OUTPUT"* ]]; then
    echo "Output is correct"
else
    echo "Output is incorrect"
    exit 1
fi

TEST2=$(cat << EOF | dividexp
adduser Lucas
adduser Eduardo
addexpense
equal
100
First expense
1
1 2
get_user_balance 2
EOF
)

EXPECTED_OUTPUT2='You owe 50.0'

if [[ "$TEST2" == *"$EXPECTED_OUTPUT2"* ]]; then
    echo "Output is correct"
else
    echo "Output is incorrect"
    exit 1
fi


exit 0
