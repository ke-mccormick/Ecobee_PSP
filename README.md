# Ecobee_PSP

This program is for anyone using an Ecobee3 or similar model thermostat that supports the Ecobee API and is a Power Smart Pricing customer.

https://www.ecobee.com/

https://www.powersmartpricing.org/

The purpose of this program is to set the Ecobee thermostat to Away if the PSP price is greater than a user defined pricing point,
and will resume the programmed schedule when the price is equal or less than the user defined pricing point.

The program also requires IFTTT webhooks called PSP_Price_High and PSP_Price_Low for notifications.
Make sure the webhook names match the names listed above and configure the applets how ever you like be notified.
https://ifttt.com/

IFTTT can be slow, so do not expect notification right away.
I have asked Power Smart Pricing to integrate with IFTTT, but that has not happened yet.

We could use IFTTT to control the Ecobee thermostat, but this can take 30 minutes to update after trigger.
Using the Ecobee API the update happens nearly instantly after triggering.

**Notice:  The files client_id.txt, IFTTT_id.txt, and tokens.txt are only examples and contain bogas data.
These files will not work, please read below on how to configure them.

IFTTT_id.txt contains the key hash for the webhooks and can be found in Maker Webhooks settings.

client_id.txt contains your Ecobee client ID for this application and is found on your Ecobee thermostat after authorizing the application.

tokens.txt is a JSON file that contains the tokens for access and token refresh provided by Ecobee.

You will need to get the information contained in the files from Ecobee and IFTTT for your specific installation.

Please begin with the Ecobee Developers page.
https://www.ecobee.com/home/developer/api/introduction/index.shtml

If you have questions, the Ecobee Developer Community maybe able to help you.
http://developer.ecobee.com/api

This application also requires the use of CURL, so be sure to have CURL installed.
https://curl.haxx.se/

All files need to be in same directory.

Usage: psp.py -n -p price

	-n		Optional: 	Enables IFTTT notification.

	-p price	Required: 	Defines the maximum Power Smart Pricing price.
	
Example: psp.py -n -p 4.3

If you do not want IFTTT notifications then leave off the -n parameter.

Max Price is the Maximum Power Smart Pricing price per kWh you are willing to pay with HVAC system running normally.

If the price becomes higher than the Max Price your thermostat will be put in away mode, reducing run time until the Power Smart Pricing price is reduced to or less than the Max Price.

You may use the Ameren Electric Supply price or whatever price you prefer.

https://www.pluginillinois.org/FixedRateBreakdownAmeren.aspx
