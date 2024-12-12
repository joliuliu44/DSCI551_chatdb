#!/bin/bash

while true; do
	yes "" | head -n 40
	echo -e "Would you like to interact with SQL or NoSQL database? (choose 1 or 2)\n1) SQL\n2) NoSQL\nAny Other Key) Exit Application"
	read -p "Your choice: " db_choice
	
	if [[ $db_choice == 1 ]]; then
		cd sql_scripts || exit
	
		while true; do
	  		yes "" | head -n 40
	    		echo "Choose an option:"
	    		echo -e "1) Input data\n2) View/Choose Databases\n3) Query Database\n4) Back"
	    		read -p "Enter an integer for your choice: " db2_choice
	
	    		case $db2_choice in
	      			1)
					yes "" | head -n 40
					python3 input_data.py
	        			;;
	      			2)
					yes "" | head -n 40
	        			python3 view_db.py
	        			continue
	        			;;
	      			3)
					yes "" | head -n 40
					./query_logic.sh
	        			;;
	      			4)
					cd ../
	        			break
	        			;;
	      			*)
	        			echo "Invalid choice. Please try again."
	        			;;
	    		esac
	  	done
	
	elif [[ $db_choice == 2 ]]; then
	  	while true; do
			yes "" | head -n 40
	    		echo "Choose an option:"
	    		echo -e "1) Input data\n2) View/Choose Databases\n3) Query Database\n4) Back"
	    		read -p "Enter an integer for your choice: " db2_choice
	
	    		case $db2_choice in
	      			1)
					yes "" | head -n 40
					python3 input_data.py
	        			;;
	      			2)
					yes "" | head -n 40
	        			python3 view_db.py
	        			continue
	        			;;
	      			3)
					yes "" | head -n 40
					./query_logic.sh
	        			;;
	      			4)
	        			break
	        			;;
	      			*)
	        			echo "Invalid choice. Please try again."
	        			;;
	    		esac
	  	done
	else
		break
	fi
done

