An Inception-v3 image detector server implemented for Raspberry Pi, based on Nodejs and SocketIO for setting up service and using Movidius NCS for accelerating inferrence.Make it convenient for use and test in distributed embedded systems.  

Now the server can communicate well with python-socketio-client. And one html is offered for interaction. 
You can use this html to send some signals to test the functionality of the server and the detector.    


Besides using one html, you can also specify your own interface with using 4 specified emit signals: "start", "infer", "exit" to control the detector, and "print message" to collect results in json format.     

node version 8.11.1 
And you need to set up Movidius NCS SDK before use.

Usage:   

cd .../RaspberryPI_nodejs_socketIO_detector  
$pip3 install socketIO-client-nexus  
$npm install   
$npm start         

And then navigate yout browser into http://localhost:3000.
This address can be modified freely.
