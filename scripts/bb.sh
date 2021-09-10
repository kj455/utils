#!/bin/bash

# helpを作成
function usage {
  cat <<EOM
Usage: $(basename "$0") [OPTION]...
  -h          Display help
  -t VALUE    body temperature
  -e          entrance form (submit entrance form)
EOM

  exit 2
}

# 引数別の処理定義
while getopts "t:eh" optKey; do
  case "$optKey" in
    t)
      python submit_temp.py ${OPTARG}
      ;;
    e)
      python submit_entry_form.py
      ;;
    '-h'|'--help'|* )
      usage
      ;;
  esac
done

exit 0
