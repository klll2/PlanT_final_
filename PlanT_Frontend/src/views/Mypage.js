import React, { useState, useEffect } from 'react';
import axios from 'axios';
// import { useCookies } from 'react-cookie';
import {
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  Table,
  Row,
  Col,
  UncontrolledDropdown, 
  DropdownToggle, 
  DropdownMenu, 
  DropdownItem,
  Button,
} from "reactstrap";

function Mypage() {
    const [trips, setTrips] = useState([]);
    const [tags, setTags] = useState([]);
    const [selectedState, setSelectedState] = useState('');
    // const [cookies, setCookie, removeCookie] = useCookies(['trvlr_id', 'trvlr_email']);
  
    useEffect(() => {
      const id = localStorage.getItem("trvlr_id");
      const fetchTrips = async () => {
          if (id) {
              try {
                const response = await axios.get(`http://localhost:8000/api/trips/?trvlr_id=${id}`);
                const filteredTrips = response.data.filter(trip => trip.trip_traveler === parseInt(id, 10));
                setTrips(filteredTrips);
                console.log(id);
                console.log(response.data);
                const tagResponse = await axios.get('http://localhost:8000/api/tags/');
                setTags(tagResponse.data);
              } catch (error) {
                  window.location.href = 'http://localhost:3000/login/login/';
              }
          } else {
              window.location.href = 'http://localhost:3000/login/login/';
          }
      };
  
      fetchTrips();
    }, []);

    const handleStateSelect = (state) => {
      setSelectedState(state);
    };

    const filteredTripsByState = selectedState === "" ? trips : trips.filter(trip => {
        const stateMap = { "예정": 1, "진행중": 2, "완료": 3 };
        return trip.trip_state === stateMap[selectedState];
    });

    const sortedTrips = filteredTripsByState.sort((a, b) => {
      const startDateA = new Date(a.trip_start);
      const startDateB = new Date(b.trip_start);
      
      if (startDateA - startDateB !== 0) {
        return startDateA - startDateB;
      }
      
      // 시작일이 같으면 종료일을 비교
      const endDateA = new Date(a.trip_end);
      const endDateB = new Date(b.trip_end);
      
      return endDateA - endDateB;
    });

    const stateToString = (state) => {
      const stateMap = { 1: "예정", 2: "진행중", 3: "완료" };
      return stateMap[state] || "";
    };

    const tagsToString = (tripTags) => {
      if (!tags.length) return '';
      const tagNames = tripTags.map(tag => {
        const foundTag = tags.find(t => t.tag_id === tag);
        return foundTag ? foundTag.tag_name : 'Unknown';
      });
      return tagNames.join(', ');
    };

    const handleDetailClick = (tripId) => {
      localStorage.setItem("trip_id", tripId);
      window.location.href = "http://localhost:3000/admin/plans";
    };

    const handleDeleteTrip = async (tripId) => {
      try {
        await axios.post("http://localhost:8000/api/trips/delete/", {tripId})
        // 삭제가 성공하면 trips를 갱신하여 새로운 상태로 업데이트
        const updatedTrips = trips.filter(trip => trip.trip_id !== tripId);
        setTrips(updatedTrips);
      } catch (error) {
        console.error('Error deleting trip:', error);
      }
    };

    return (
      <>
        <div className="content">
          <Row>
              <Col md="12">
                  <Card>
                  <CardHeader>
                      <CardTitle tag="h4">My Trips</CardTitle>
                  </CardHeader>
                  <CardBody>
                    <div className="text-right">
                      <UncontrolledDropdown group>
                          <DropdownToggle caret color="info">
                              State
                          </DropdownToggle>
                          <DropdownMenu>
                            <DropdownItem onClick={() => handleStateSelect("")}>All</DropdownItem>
                            <DropdownItem onClick={() => handleStateSelect("예정")}>예정</DropdownItem>
                            <DropdownItem onClick={() => handleStateSelect("진행중")}>진행 중</DropdownItem>
                            <DropdownItem onClick={() => handleStateSelect("완료")}>완료</DropdownItem>
                          </DropdownMenu>
                      </UncontrolledDropdown>
                    </div>
                <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
                  <table className="table table-hover">
                    <thead className="text-primary">
                        <tr>
                        <th>Start Date</th>
                        <th>End Date</th>
                        <th>Tags</th>
                        <th>State</th>
                        <th>Detail</th>
                        <th>Delete</th>
                        </tr>
                    </thead>
                    <tbody>
                        {sortedTrips.map((trip, index) => (
                        <tr key={index}>
                            <td>{trip.trip_start}</td>
                            <td>{trip.trip_end}</td>
                            <td>{tagsToString(trip.trip_tags)}</td>
                            <td>{stateToString(trip.trip_state)}</td>
                            <td>
                            <Button
                              block
                              className="btn-round" 
                              color="primary" 
                              onClick={() => handleDetailClick(trip.trip_id)}>
                              Detail 
                            </Button>
                            </td>
                            <td>
                            <Button
                              className="btn-round" 
                              color="danger" 
                              onClick={() => handleDeleteTrip(trip.trip_id)}>
                              Delete
                            </Button>
                            </td>
                        </tr>
                        ))}
                    </tbody>
                  </table>
                </div>
                    <br/>
                    <br/>
                    <hr/>
                    <br/>
                    <Col className="ml-auto mr-auto" lg="8">
                      <Row>
                        <Col md="4">
                          {/* <Button 
                            block
                            className="btn-round" 
                            color="primary"
                            href="http://localhost:3000/admin/icons">
                            Prev
                          </Button> */}
                        </Col>
                        <Col md="4">
                        </Col>
                        <Col md="4">
                          <Button 
                            block
                            className="btn-round" 
                            color="primary" 
                            type="submit"
                            href="http://localhost:3000/admin/icons">
                            New Trip
                          </Button>
                        </Col>
                      </Row>
                    </Col>  
                  </CardBody>
                  </Card>
              </Col>
          </Row>
        </div>
      </>
    );
}

export default Mypage;
