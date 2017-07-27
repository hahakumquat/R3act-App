# R3actApp

Detects falls with a machine learning algorithm using accelerometer data collected from an Android device.

# Tech Stack

Front End:
- React Native
  - native-base
  - react-native-communications
  - react-native-send-intent
  - react-native-sensors

Back End:
- Flask Server
- Python
  - scipy 

# Appendix

Data found here, use V2: http://www.bmi.teicrete.gr/index.php/research/mobiact

To test, open a terminal and do the following:

export FLASK_APP=main.py

python -m flask run
