//import express from 'express';
//import path from 'path';
//import bodyParser from 'body-parser';


const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const app = express();
const server = require('http').createServer(app);
const io = require('socket.io').listen(server);
const PORT = 3000;
server.listen(PORT);
console.log('Server is running');

const users = [];
const connections = [];
var exec = require('child_process').exec;
io.sockets.on('connection',(socket) => {
   connections.push(socket);
   console.log(' %s sockets is connected', connections.length);
   if (connections.length == 1){
      exec('./client_sio.py',function(error,stdout,stderr){
         if(error){
            console.log('error: '+error);
            io.sockets.emit('print message', {message: error});
         }
         if(stderr){
            console.log('stderr: '+stderr);
            io.sockets.emit('print message', {message: stderr});
         }
      }); 
   }

   socket.on('disconnect', () => {
      connections.splice(connections.indexOf(socket), 1);
   });
   

   socket.on('new message', (message) => {
      console.log('I got a new message from Client:', message);
      io.sockets.emit('print message', {message:message});
   });

   socket.on('start message', () => {
      console.log('Start Message from html.');
      io.sockets.emit('start');

   });

   socket.on('infer message', () => {
      console.log('Infer Message from html.');
      io.sockets.emit('infer');
   });

   socket.on('exit message', () => {
      console.log('Exit Message from html.');
      io.sockets.emit('exit');
   });
});

app.get('/', (req, res) => {
   res.sendFile(__dirname + '/index.html');
});
