# Open terminal at current directory which this script file exists and execute the command.
chmod +x ./install_requirements.sh

# Install python module on the terminal
./install_requirements.sh

# Copy your text based model to database_model.txt

# Execute below command to run this script on background
nohup python3 ./chatgpt_clipboard_sql.py &

# To stop running this script
pkill -f chatgpt_clipboard_sql.py

# You can change your api-key at line 46

# You can change the model by changing the model at line 81

# You can see the log in chatgpt_clipboard_sql_log.log file