from subprocess import check_output
import datetime
import getopt
import json
import os
import sys
import time
import urllib.request

# Returns client id from file client_id.txt as string.
def get_file_path(file):
    file_path = os.path.join(sys.path[0], file)
    return file_path

# Returns JSON string value from JSON file as string.
def get_JSON_string_value(file, string):
    key_file = open(get_file_path(file), 'r')
    key_data = json.loads(key_file.read())
    return key_data[string]

# Returns client id from file client_id.txt as string.
def get_client_id():
    client_file = open(get_file_path('client_id.txt'), 'r')
    client_id = client_file.read()
    return client_id

# Returns refresh token from JSON file tokens.txt as string.
def get_refresh_token():
    refresh_token = get_JSON_string_value('tokens.txt','refresh_token')
    return refresh_token

# Returns refresh token from JSON file tokens.txt as string.
def get_access_token():
    access_token = get_JSON_string_value('tokens.txt','access_token')
    return access_token

# Excutes CURL command to refresh keys stored in JSON file tokens.txt
def refresh_keys():
    refresh_token = get_refresh_token()
    client_id = get_client_id()
    refresh = 'curl -s -X POST "https://api.ecobee.com/token?grant_type=refresh_token&refresh_token=' + refresh_token + '&client_id=' + client_id + '" -o tokens.txt'
    check_output(refresh, shell=True).decode()
    return None

# Returns the current PSP hourly price as string.
def get_psp_price():
    psp_request = urllib.request.Request('https://www.powersmartpricing.org/psp/servlet?type=instantHOURlyfullsite')
    psp_response = urllib.request.urlopen(psp_request)
    psp_price_string = psp_response.read()
    psp_price_elements = psp_price_string.split()
    current_psp_price = psp_price_elements[3].decode()
    return current_psp_price

# Execute Ecobee command file.
def execute_Ecobee_command_file(command_file):
    refresh_keys() # Access Tokens expire hour, best to refresh before execution.
    access_token = get_access_token()
    file_path = get_file_path(command_file)
    command = 'curl -s -X POST --data-urlencode @' + file_path + ' -H "Content-Type: application/json;charset=UTF-8" -H "Authorization: Bearer ' + access_token + '" "https://api.ecobee.com/1/thermostat?format=json"'
    check_output(command, shell=True).decode()
    return None

# IFTTT Execute Event
def IFTTT_execute(event):
    IFTTT_file = open(get_file_path('IFTTT_id.txt'), 'r')
    IFTTT_id = IFTTT_file.read()
    command = 'curl -s -X POST https://maker.ifttt.com/trigger/' + event + '/with/key/' + IFTTT_id
    check_output(command, shell=True).decode()
    return None

# Set Ecobee away indefinitely.
def set_away_indefinitely():
    execute_Ecobee_command_file('indefinite_away.txt')
    print('Setting Away Indefinitely')
    return None

# Set Ecobee resume program.
def set_resume_program():
    execute_Ecobee_command_file('resume_program.txt')
    print('Resuming Programming')
    return None

# Print Press ENTER to exit message and exit after user hits ENTER.
def press_ENTER_exit_message():
    input('\n' + 'Press ENTER to exit')
    sys.exit()
    return None

# Print file usage statement.
def usage():
    print('Usage: psp.py -n -p price')
    print('-n        Optional: Enables IFTTT notification.')
    print('-p price  Required: Defines the maximum Power Smart Pricing price.')
    return None

# Clears the output window.
def clear_output_window():
    os.system('cls' if os.name=='nt' else 'clear')
    return None

# Returns current system time.
def get_system_time():
    time = datetime.datetime.time(datetime.datetime.now())
    return time

# Returns current system hour as integer.
def get_system_hour():
    hour = get_system_time().strftime('%H')
    return int(hour)

# Returns current system minute as integer.
def get_system_minute():
    minute = get_system_time().strftime('%M')
    return int(minute)

# Main.
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],'hnp:',['help','notify','price='])
    except getopt.GetoptError as err:
        print(err)
        usage()
        press_ENTER_exit_message()
    # If no parameters.    
    if not opts:
        print('option -p is required')
        usage()
        press_ENTER_exit_message()

    IFTTT_notify = False
    max_price = float(-1)

    for opt, arg in opts:
        if opt in ('-h','--help'):
            usage()
            press_ENTER_exit_message()
        elif opt in ('-n', '--notify'):
            IFTTT_notify = True
        elif opt in ('-p', '--price'):
            try:
               max_price = float(arg)
            except ValueError:
                usage()
                press_ENTER_exit_message()  
        else:
            assert False, "unhandled option"

    # Max Price must be set.
    if(max_price == -1):
        print('option -p is required')
        usage()
        press_ENTER_exit_message()

    # Keep track of last change.
    previous_hour = -1
    current_hour = get_system_hour()
    current_price = float(0)
    PSP_delay = 15
    PSP_High = -1
    
    # Need loop here.
    while(True):
        # Check for time change.
        while(previous_hour == current_hour):
            time.sleep(1) # Delay for 1 seconds.
            current_hour = get_system_hour() # Update current hour.
        # If hour has just changed, wait for PSP website to updated price.
        if(get_system_minute() == 0):
            clear_output_window()
            print('Updating Current PSP Price')
            print('Please Wait ' + str(PSP_delay) + ' Seconds...')
            time.sleep(PSP_delay) # Delay for PSP_delay number of seconds.
            clear_output_window()
        previous_hour = current_hour # Update previous hour to current hour.
        print('Update Triggered at ' + get_system_time().strftime('%H:%M:%S')) # Display Current Time
        print('Max Price is ' + str(max_price)) # Print Max Price
        current_price = float(get_psp_price()) # Update Current Price
        print('Current Price is ' + str(current_price)) # Display Current Price
        # If current price is cheaper than max price, resume program else set away indefinitely.
        if(current_price <= max_price):
            print('Current Price Less Than Or Equal To Max Price')
            set_resume_program()
            # Notify once when price changed.
            if(IFTTT_notify == True and PSP_High != 0):
                IFTTT_execute('PSP_Price_Low_Notify')
            PSP_High = 0
        else:
            print('Current Price Greater Than Max Price')
            set_away_indefinitely()
            # Notify once when price changed.
            if(IFTTT_notify == True and PSP_High != 1):
                IFTTT_execute('PSP_Price_High_Notify')
            PSP_High = 1
        print('Please Wait For Next Hourly Update...')

    press_ENTER_exit_message()

if __name__ == "__main__":
    main()
