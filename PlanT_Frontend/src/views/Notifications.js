import React, { useState, useEffect } from "react";
import NotificationAlert from "react-notification-alert";
import {
  Button,
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  Row,
  Col,
  Table,
  Nav,
  NavItem,
  NavLink,
  UncontrolledDropdown, 
  DropdownToggle, 
  DropdownMenu, 
  DropdownItem
} from "reactstrap";
import logo from '../plant.png'
import MapWrapper from "./Mapwraper";
import axios from "axios";


function Notifications() {
  const notificationAlert = React.useRef();

  const placeIds = [2, 1, 12, 19, 26];
  const notify = (message) => {
    var color = Math.floor(Math.random() * 5 + 1);
    var type;
    switch (color) {
      case 1:
        type = "primary";
        break;
      case 2:
        type = "success";
        break;
      case 3:
        type = "danger";
        break;
      case 4:
        type = "warning";
        break;
      case 5:
        type = "info";
        break;
      default:
        break;
    }
    var options = {};
    options = {
      place: "tc",
      message: (
        <div>
          <div>
           {message}
          </div>
        </div>
      ),
      type: type,
      // icon: "nc-icon nc-bell-55",
      autoDismiss: 7,
    };
    notificationAlert.current.notificationAlert(options);
  };


  const [clientPlans, setClientPlans] = useState({});
  const [selectedButton, setSelectedButton] = useState('');
  const [plcNames, setPlcNames] = useState([]);
  const [plcTimes, setPlcTimes] = useState([]);
  const [plnScore, setPlnScore] = useState("");

  useEffect(() => {

    const formatDate = (dateStr) => {
      const date = new Date(dateStr);
      const year = date.getFullYear();
      const month = ('0' + (date.getMonth() + 1)).slice(-2);
      const day = ('0' + date.getDate()).slice(-2);
      return `${year}-${month}-${day}`;
    };

    const fetchData = async () => {
      try {
        const data = {
          trvlr_id: localStorage.getItem('trvlr_id'),
          start_date: formatDate(localStorage.getItem('start_date')),
          end_date: formatDate(localStorage.getItem('end_date')),
          selected_tags: JSON.parse(localStorage.getItem('selected_tags')).map(tag => tag.id)
        };

        const response = await axios.post('http://localhost:8000/account/plans/new/', data);
        console.log(response.data);
        const { plc_names, plc_times, pln_score } = response.data;
        setPlcNames(plc_names);
        setPlcTimes(plc_times);
        setPlnScore(pln_score);
      } catch (error) {
        console.error('Error:', error);
      }
    };
    fetchData();
  }, []);


  // const handleTagSelect = (tag) => {
  //   setSelectedTag(tag); // 선택된 태그 업데이트
  // };

  // const handleButtonSelect = (button) => {
  //   setSelectedButton(button); // 선택된 태그 업데이트
  // };

  // const handletableSelect = (table) => {
  //   setSelectedtable(table); // 선택된 태그 업데이트
  // };



  const handleButtonClick = (message) => {
    notify(message);
  };

  return (
    <>
      <div className="content">
        <NotificationAlert ref={notificationAlert} />
        <Row>
          <Col md="12">
            <Card>
              <CardHeader>
                <CardTitle tag="h5">Plans by PlanT</CardTitle>
                <Nav tabs>
                  <NavItem>
                    <NavLink href="#" active>1일차</NavLink>
                  </NavItem>
                  <NavItem>
                    <NavLink href="#">2일차</NavLink>
                  </NavItem>
                </Nav>
              </CardHeader>
              <CardBody>
                <Row>
                  <Col md="6">
                    <Card className="card-plain">
                      <CardHeader>
                        <CardTitle tag="h5">Daily Schedule</CardTitle>
                      </CardHeader>
                      <CardBody>
                      <hr/>
                      <div className="text-center">
                          {plcNames.map((place, index) => (
                            <div key={index}>
                              <Button color="success" fade={false}>
                                <span>{place}</span>
                              </Button>
                              <br />
                              {index < plcTimes.length / 2 && (
                                <Button color="secondary" onClick={() => handleButtonClick(plcTimes[2 * index]+ "~" + plcTimes[2 * index + 1])}>
                                  <span> + </span>
                                </Button>
                              )}
                              <br />
                            </div>
                          ))}
                        </div>
                      </CardBody>
                    </Card>
                  </Col>
                  <Col md="6">
                    <Card className="card-plain">
                      <CardHeader>
                        <CardTitle tag="h5">Display On Map</CardTitle>
                      </CardHeader>
                      <CardBody>
                      <hr />
                      <div
                        id="map"
                        className="map"
                        style={{ position: "relative", overflow: "hidden" }}
                      >
                        <MapWrapper placeIds={placeIds} />
                      </div>
                      </CardBody>
                      <hr/>
                      <p>{ plnScore }</p>
                    </Card>
                  </Col>
                </Row>
              </CardBody>
              <br />
              <br />
              <hr />
              <br />
              <div>
                <Col className="ml-auto mr-auto" lg="8">
                  <Row>
                    <Col md="4">
                      <Button
                        block
                        className="btn-round"
                        color="primary"
                        href="http://localhost:3000/admin/icons">
                        Prev
                      </Button>
                    </Col>
                    <Col md="4">
                    </Col>
                    <Col md="4">
                      <Button
                        block
                        className="btn-round"
                        color="primary"
                        type="submit"
                        href="http://localhost:3000/admin/mypage">
                        Home
                      </Button>
                    </Col>
                  </Row>
                </Col>
              </div>
            </Card>
          </Col>
        </Row>
      </div>
    </>
  );
}

export default Notifications;