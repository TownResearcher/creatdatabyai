import { io } from 'socket.io-client';
import { useEffect, useState } from 'react';

const SOCKET_URL = 'http://localhost:5000';

export const useSocket = () => {
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const socketIo = io(SOCKET_URL);

    socketIo.on('connect', () => {
      console.log('Connected to WebSocket server');
    });

    socketIo.on('disconnect', () => {
      console.log('Disconnected from WebSocket server');
    });

    setSocket(socketIo);

    return () => {
      socketIo.disconnect();
    };
  }, []);

  return socket;
}; 