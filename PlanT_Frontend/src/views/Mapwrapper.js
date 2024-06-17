import React, { useEffect, useRef, useState } from "react";
import axios from 'axios';

// reactstrap components

const MapWrapper = ({ placeIds }) => {
  const mapRef = useRef(null);
  const [placeCoordinates, setPlaceCoordinates] = useState({});

  useEffect(() => {
    const fetchPlaceDetails = async () => {
      try {
        const placeCoordinatesTemp = {};
        for (const placeId of placeIds) {
          const response = await axios.get(`http://localhost:8000/api/places/${placeId}`);
          const place = response.data;
          placeCoordinatesTemp[place.place_id] = {
            lat: place.place_latitude,
            lng: place.place_longitude,
            title: place.place_name,
          };
          console.log(placeId, place, placeCoordinatesTemp[place.id])
        }
        setPlaceCoordinates(prevState => ({
          ...prevState,
          ...placeCoordinatesTemp
        }));
      } catch (error) {
        console.error("Error fetching place details:", error);
      }
    };

    fetchPlaceDetails();
  }, [placeIds]);

  useEffect(() => {
    if (Object.keys(placeCoordinates).length === 0) return;

    let google = window.google;
    let map = mapRef.current;

    const mapOptions = {
      zoom: 13,
      center: { lat: 37.497917, lng: 127.027628 },
      scrollwheel: false,
      zoomControl: true,
      styles: [
        // 지도 스타일 설정
      ],
    };

    map = new google.maps.Map(mapRef.current, mapOptions);

    const markers = []; // 마커 정보를 저장할 배열
    const lines = []; // 선 정보를 저장할 배열
    const bounds = new google.maps.LatLngBounds(); // 모든 장소를 포함하는 경계를 설정할 객체

    placeIds.forEach((placeId, index) => {
      const placeInfo = placeCoordinates[placeId];
      if (!placeInfo) return; // 장소 정보가 없으면 종료

      const position = new google.maps.LatLng(placeInfo.lat, placeInfo.lng);
      bounds.extend(position); // 경계에 좌표 추가

      // 마커 생성
      const marker = new google.maps.Marker({
        position,
        map,
        title: placeInfo.title,
      });

      // 마커를 markers 배열에 추가
      markers.push(marker);

      // 정보창 생성
      const contentString = `<div class="info-window-content"><h2>${placeInfo.title}</h2>` +
        `<p>Marker content here.</p></div>`;
      const infowindow = new google.maps.InfoWindow({
        content: contentString,
      });

      // 마커를 클릭했을 때 정보창 열기
      google.maps.event.addListener(marker, "click", function () {
        infowindow.open(map, marker);
      });

      // 경로를 그리기 위한 로직
      if (index < placeIds.length - 1) {
        // 다음 장소의 정보
        const nextPlaceId = placeIds[index + 1];
        const nextPlaceInfo = placeCoordinates[nextPlaceId];
        if (!nextPlaceInfo) return; // 다음 장소 정보가 없으면 종료

        const nextPosition = new google.maps.LatLng(nextPlaceInfo.lat, nextPlaceInfo.lng);

        // 선을 그리고 지도에 추가
        const line = new google.maps.Polyline({
          path: [position, nextPosition],
          geodesic: true,
          strokeColor: "#FF0000",
          strokeOpacity: 0.5,
          strokeWeight: 4,
          icons: [{
            icon: {
              path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
            },
            offset: "100%",
          }],
        });
        line.setMap(map);
        lines.push(line);
      }
    });

    // 모든 마커가 보이도록 지도 시점을 조절
    map.fitBounds(bounds);
  }, [placeCoordinates, placeIds]);

  return <div style={{ height: `100%` }} ref={mapRef}></div>;
};

export default MapWrapper;