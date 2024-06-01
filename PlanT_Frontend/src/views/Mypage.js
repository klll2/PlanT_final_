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

    const stateToString = (state) => {
      const stateMap = { 1: "예정", 2: "진행중", 3: "완료" };
      return stateMap[state] || "";
    };

    const TagToString = (tag) => {
      const tagMap = { 1: "None", 2: "바다여행", 3: "시장투어" };
      return tagMap[tag] || "";
    };

    const handleDetailClick = (tripId) => {
      localStorage.setItem("trip_id", tripId);
      window.location.href = "http://localhost:3000/admin/plans";
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
                    <Table responsive>
                    <thead className="text-primary">
                        <tr>
                        <th>Start Date</th>
                        <th>End Date</th>
                        <th>Tags</th>
                        <th>State</th>
                        <th>Detail</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredTripsByState.map((trip, index) => (
                        <tr key={index}>
                            <td>{trip.trip_start}</td>
                            <td>{trip.trip_end}</td>
                            <td>{TagToString(trip.trip_tag)}</td>
                            <td>{stateToString(trip.trip_state)}</td>
                            <td><Button
                            block
                            className="btn-round" 
                            color="primary" 
                            onClick={() => handleDetailClick(trip.trip_id)}>
                            Detail </Button></td>
                        </tr>
                        ))}
                    </tbody>
                    </Table>
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
