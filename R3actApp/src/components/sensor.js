import React, { Component } from 'react';
import { DeviceEventEmitter, ToastAndroid, StyleSheet, View, AsyncStorage } from 'react-native';
import { Container, Header, Content, Footer, FooterTab, Button, Text, Icon, H1, Form, Item, Input} from 'native-base';
import { decorator as sensors} from 'react-native-sensors';
import RNSensors from 'react-native-sensors';
import Communications from 'react-native-communications';
import SendSMS from 'react-native-sms'

var dataPoints = [];
var interval = 100; // 1ms
var time = 0;
var server = 'http://10.104.106.183:3000';
var isTrackScreen = true;

const { Accelerometer } = RNSensors;
const accelerationObservable = new Accelerometer({
  updateInterval: interval,
});

// const gyroscopeObservable = new Gyroscope({
//   updateInterval: interval,
// });

DeviceEventEmitter.addListener('Accelerometer', function(data) {
  var SendIntentAndroid = require('react-native-send-intent');
  time = time + interval;
  dataPoints.push(
  {
    "t": time, 
    "x": data.x,
    "y": data.y,
    "z": data.z
  }
  );
  var contactName = '';
  var contactNumber = '';
  var age = '';
  var gender = '';
  var height = '';
  var weight ='';
  if(time % 10000 == 0) {
    AsyncStorage.getItem('contact').then((value) => {
      contactName = value;
    }).done();
    AsyncStorage.getItem('number').then((value) => {
      contactNumber = value;
    }).done();
    AsyncStorage.getItem('age').then((value) => {
      age = value;
    }).done();
    AsyncStorage.getItem('gender').then((value) => {
      gender = value;
    }).done();
    AsyncStorage.getItem('height').then((value) => {
      height = value;
    }).done();
    AsyncStorage.getItem('weight').then((value) => {
      weight = value;
    }).done();
    data = JSON.stringify({
        "name": contactName,
        "number" : contactNumber,
        "age" : age,
        "gender" : gender,
        "height" : height,
        "weight" : weight,
        "results" : dataPoints,
      });
    // ToastAndroid.show(data, ToastAndroid.SHORT);
    fetch(server, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: data
    }).then((response) => response.text())
      .then((responseText) => {
        var fallen = JSON.parse(responseText);
        if(fallen['fallen'] == 'Fall') {
          ToastAndroid.show(fallen['fallen'] + " - Calling " + contactNumber , ToastAndroid.SHORT);
          SendIntentAndroid.sendPhoneCall(contactNumber);
        }
      })
      .catch((error) => {
        ToastAndroid.show('ERROR: ' + error, ToastAndroid.SHORT);
      });
      dataPoints = [];
  }
  // if (data.x > 4 || data.y > 4) {
    // SendIntentAndroid.sendPhoneCall('2487033234')
    // ToastAndroid.show(JSON.stringify(dataPoints), ToastAndroid.SHORT);
    // Communications.phonecall('2487033234', true);
    // Communications.text('2487033234');
  //}
});

// function trackScreen() {
//   isTrackScreen = !isTrackScreen;
//   ToastAndroid.show(isTrackScreen.toString(), ToastAndroid.SHORT);
// }

export default class sensor extends Component {

  constructor(props) {
    super(props);
    this.state = {
      acceleration: {
        x: 'unknown',
        y: 'unknown',
        z: 'unknown',
      },
      gyroscope: {
        x: 'unknown',
        y: 'unknown',
        z: 'unknown',
      }
    };
  }

  componentWillMount() {
    accelerationObservable
      .subscribe(acceleration => this.setState({
        acceleration,
      }));

    // gyroscopeObservable
    //   .subscribe(gyroscope => this.setState({
    //     gyroscope,
    //   }));
  }

  navToTrackPage() {
    isTrackScreen = true;
    ToastAndroid.show("Track pressed", ToastAndroid.SHORT);
  }

  navToContactPage() {
    isTrackScreen = false;
    ToastAndroid.show("Contact pressed", ToastAndroid.SHORT);
  }

  saveData(key, value) {
    AsyncStorage.setItem(key, value);
    //this.setState({key: value});
    // AsyncStorage.getItem(key).then((value) => {
    //   ToastAndroid.show(value, ToastAndroid.SHORT);
    // }).done();
  }

  render() {
    const {
      acceleration,
      // gyroscope,
    } = this.state;

    return (
      <Container>
        <Header />
        <Content>
          {isTrackScreen ? (
          <View style={styles.container}>
            <H1 style={styles.welcome}>
              Tracker Data
            </H1>
            <Text style={styles.welcome}>
              Acceleration:
            </Text>
            <Text style={styles.instructions}>
              x: {acceleration.x}
            </Text>
            <Text style={styles.instructions}>
              y: {acceleration.y}
            </Text>
            <Text style={styles.instructions}>
              z: {acceleration.z}
            </Text>
          </View>
          ) : (
          <View>
            <Form>
              <Item>
                <Input placeholder="Contact Name" onChangeText={(text) => this.saveData('contact', text)} />
              </Item>
              <Item last>
                <Input placeholder="Contact Number" onChangeText={(text) => this.saveData('number', text)} />
              </Item>
              <Item>
                <Input placeholder="Age" onChangeText={(text) => this.saveData('age', text)} />
              </Item>
              <Item last>
                <Input placeholder="Gender" onChangeText={(text) => this.saveData('gender', text)}/>
              </Item>
              <Item>
                <Input placeholder="Height" onChangeText={(text) => this.saveData('height', text)}/>
              </Item>
              <Item last>
                <Input placeholder="Weight" onChangeText={(text) => this.saveData('weight', text)}/>
              </Item>
            </Form>
          </View>
          )}
        </Content>    
        <Footer>
          <FooterTab>
            <Button vertical active onPress={() => this.navToTrackPage()}>
              <Icon name="apps" />
              <Text>Tracker</Text>
            </Button>
            <Button vertical active onPress={() => this.navToContactPage()}>
              <Icon name="person" />
              <Text>Contact</Text>
            </Button>
          </FooterTab>
        </Footer>
      </Container>       
    );
  }

  componentWillUnmount() {
    accelerationObservable.stop();
    gyroscopeObservable.stop();
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5FCFF',
  },
  welcome: {
    marginTop: 30,
    fontSize: 20,
    textAlign: 'center',
    margin: 10,
  },
  instructions: {
    textAlign: 'center',
    color: '#333333',
    marginBottom: 5,
  },
});