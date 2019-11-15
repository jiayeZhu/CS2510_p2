for((i = 0; i < $1; i++))
do
  python3 -u ClientBot.py -d cbot_$[0+$i] -M $2 -N $3 -r $4 -f $5 >client_$[0+$i].log &
done