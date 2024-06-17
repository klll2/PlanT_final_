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
  Nav,
  NavItem,
  NavLink,
  TabContent,
  TabPane,
} from "reactstrap";
import classnames from "classnames";
import MapWrapper from "./Mapwrapper";
import PlanDetails from "./PlanDetails";
import axios from "axios";

function Notifications() {
  const notificationAlert = React.useRef();

  const [clientPlans, setClientPlans] = useState({});
  const [activeTab, setActiveTab] = useState('1');
  const [placeIds, setPlaceIds] = useState([]);
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
      const trip_id = localStorage.getItem('trip_id')
      if (trip_id) {
        const trip_data = { 'trip_id' : trip_id }
        try {
          const response = await axios.post('http://localhost:8000/account/plans/new/map/', trip_data);
          if (response) {
            const plans = response.data; // 서버로부터 받은 이중 딕셔너리 데이터
            console.log(plans)
            setClientPlans(plans);
            setPlaceIds(plans['1'].plc_ids); // 첫 번째 탭에 해당하는 placeIds 설정
            setPlnScore(plans['1'].pln_score);
            console.log(plnScore, plans['1'].pln_score)
          }
        } catch (error) {
          console.error('Error:', error);
        }
      }
      else {
        try {
          let datas = {}; // let 키워드를 사용하여 재할당 가능하도록 선언합니다.

          if (localStorage.getItem('selected_tags')) {
            datas = {
              trvlr_id: localStorage.getItem('trvlr_id'),
              start_date: formatDate(localStorage.getItem('start_date')),
              end_date: formatDate(localStorage.getItem('end_date')),
              selected_tags: localStorage.getItem('selected_tags'),
              query: "",
            };
          } else {
            datas = {
              trvlr_id: localStorage.getItem('trvlr_id'),
              start_date: formatDate(localStorage.getItem('start_date')),
              end_date: formatDate(localStorage.getItem('end_date')),
              selected_tags: [],
              query: localStorage.getItem('input_query'),
            };
          }
          console.log(datas);
          const response = await axios.post('http://localhost:8000/account/plans/new/', datas);
          if (response) {
            const plans = response.data; // 서버로부터 받은 이중 딕셔너리 데이터
            console.log(plans)
            setClientPlans(plans);
            setPlaceIds(plans['1'].plc_ids); // 첫 번째 탭에 해당하는 placeIds 설정
            setPlnScore(plans['1'].pln_score);
          }
        } catch (error) {
          console.error('Error:', error);
        }
      }
    };
    fetchData();
  }, []);

  const handleReset = () => {
    localStorage.removeItem('trip_id');
    localStorage.removeItem('start_date');
    localStorage.removeItem('end_date');
    localStorage.removeItem('selected_tags');
  };

  const toggle = tab => {
    console.log(tab, activeTab, placeIds, clientPlans[tab].plc_ids, clientPlans)
    if (activeTab !== tab) {
      setActiveTab(tab);
      setPlaceIds(clientPlans[tab].plc_ids); // 탭 변경 시 placeIds 업데이트 
      console.log(tab, activeTab, placeIds, clientPlans[tab].plc_ids, clientPlans)
    }
  };

  // const formatPlnScore = (plnScore) => {
  //   return Object.entries(plnScore).map(([key, value]) => `${key} : ${value}`).join(', ');
  // };


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
                  {Object.keys(clientPlans).map((key) => (
                    <NavItem key={key}>
                      <NavLink
                        className={classnames({ active: activeTab === key })}
                        onClick={() => { toggle(key); }}
                      >
                        {key}일차
                      </NavLink>
                    </NavItem>
                  ))}
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
                        <TabContent activeTab={activeTab}>
                          {Object.keys(clientPlans).map((key) => (
                            <TabPane tabId={key} key={key}>
                              <PlanDetails 
                                plcNames={clientPlans[key].plc_names} 
                                plcTimes={clientPlans[key].plc_times}
                              />
                            </TabPane>
                          ))}
                        </TabContent>
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
                      <br/>
                      <hr />
                    </Card>
                  </Col>
                </Row>
              </CardBody>
              <CardBody className="text-center">
                <h5>추천 점수 : {plnScore} 점 </h5>
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
                        onClick={handleReset}
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
