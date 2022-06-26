#!/bin/bash

TEST=$(cat << EOF | dividexp
adduser LucasL
adduser LucasS
adduser Eduardo
addexpense
percentage
100
First expense
1
1 2 3
20 30 50
get_user_balance 1
EOF
)

TEST_EXPECTED_OUTPUT='You are owed 80.0'

if [[ "$TEST" == *"$TEST_EXPECTED_OUTPUT"* ]]; then
    echo "TEST success"
else
    echo "TEST failed. Expected user 1 balance to contain: ${TEST_EXPECTED_OUTPUT}, but got:"
    echo $TEST
    exit 1
fi

TEST2=$(cat << EOF | dividexp
adduser LucasL
adduser LucasS
adduser Eduardo
addexpense
percentage
100
First expense
1
1 2 3
20 30 50
get_user_balance 2
EOF
)

TEST2_EXPECTED_OUTPUT='You owe 30.0'

if [[ "$TEST2" == *"$TEST2_EXPECTED_OUTPUT"* ]]; then
    echo "TEST2 success"
else
    echo "TEST2 failed. Expected user 2 balance to contain: ${TEST2_EXPECTED_OUTPUT}, but got:"
    echo $TEST2
    exit 1
fi

TEST3=$(cat << EOF | dividexp
adduser LucasL
adduser LucasS
adduser Eduardo
addexpense
percentage
100
First expense
1
1 2 3
20 30 50
get_user_balance 3
EOF
)

TEST3_EXPECTED_OUTPUT='You owe 50.0'

if [[ "$TEST3" == *"$TEST3_EXPECTED_OUTPUT"* ]]; then
    echo "TEST3 success"
else
    echo "TEST3 failed. Expected user 3 balance to contain: ${TEST3_EXPECTED_OUTPUT}, but got:"
    echo $TEST3
    exit 1
fi

exit 0