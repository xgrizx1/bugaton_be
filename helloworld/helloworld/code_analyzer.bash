#!/bin/bash

commitNew=$1
commitOld=$2
gitUrl=$3

git pull --all

git_changes=$(git diff --shortstat <commit1> <commit2>)

git checkout commitNew

 