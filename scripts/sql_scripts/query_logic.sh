#!/bin/bash

while true; do
  yes "" | head -n 40
	echo "Choose a query option:"
	echo -e "1) Get example queries\n2) Explore query commands\n3) Run your own query\n4) Back"
	read -p "Choice: " query_choice

	case $query_choice in
		1)
			yes "" | head -n 40
			python3 general_sample_query.py
			;;
		2)
			yes "" | head -n 40
			python3 sample_query.py
			;;
		3)
			yes "" | head -n 40
			python3 nlp.py
			python3 run_query.py
			;;
		4)
			break
			;;
		*)
			echo "Invalid choice. Please try again."
			;;
	esac
done