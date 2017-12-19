#!/bin/bash

ls *\,* >/dev/null 2>&1
if [ "${?}" == "0" ]; then
  ls *\,* | xargs rm
fi
  
ls .*\,* >/dev/null 2>&1
if [ "${?}" == "0" ]; then
  ls .*\,* | xargs rm
fi
  
ls *::* >/dev/null 2>&1
if [ "${?}" == "0" ]; then
  ls *::* | xargs rm
fi
  
ls .*::* >/dev/null 2>&1
if [ "${?}" == "0" ]; then
  ls .*::* | xargs rm
fi
  
ls *\(* >/dev/null 2>&1
if [ "${?}" == "0" ]; then
  ls *\(* | xargs rm
fi
  
ls .*\(* >/dev/null 2>&1
if [ "${?}" == "0" ]; then
  ls .*\(* | xargs rm
fi
  
ls *\)* >/dev/null 2>&1
if [ "${?}" == "0" ]; then
  ls *\)* | xargs rm
fi
  
ls .*\)* >/dev/null 2>&1
if [ "${?}" == "0" ]; then
  ls .*\)* | xargs rm
fi
  
ls *\<* >/dev/null 2>&1
if [ "${?}" == "0" ]; then
  ls *\<* | xargs rm
fi
  
ls .*\<* >/dev/null 2>&1
if [ "${?}" == "0" ]; then
  ls .*\<* | xargs rm
fi
  
ls *\>* >/dev/null 2>&1
if [ "${?}" == "0" ]; then
  ls *\>* | xargs rm
fi
  
ls .*\>* >/dev/null 2>&1
if [ "${?}" == "0" ]; then
  ls .*\>* | xargs rm
fi
  
