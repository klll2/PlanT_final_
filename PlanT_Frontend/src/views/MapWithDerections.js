import React, { useState } from 'react';
import { DirectionsRenderer, GoogleMap, LoadScript } from '@react-google-maps/api';

const MapWithDirections = ({ origin, destination }) => {
  const [directions, setDirections] = useState(null);

  const directionsCallback = (response) => {
    if (response !== null) {
      setDirections(response);
    }
  };

  return (
    <LoadScript googleMapsApiKey="YOUR_API_KEY">
      <GoogleMap
        id="directions-map"
        mapContainerStyle={{
          width: '100%',
          height: '400px'
        }}
        zoom={10}
        center={{ lat: 37.497917, lng: 127.027628 }}
      >
        {origin && destination && (
          <DirectionsService
            options={{
              destination: destination,
              origin: origin,
              travelMode: 'DRIVING'
            }}
            callback={directionsCallback}
          />
        )}
        {directions && <DirectionsRenderer directions={directions} />}
      </GoogleMap>
    </LoadScript>
  );
};

export default MapWithDirections;
