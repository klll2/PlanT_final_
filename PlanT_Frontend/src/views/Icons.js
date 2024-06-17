import React, { useState, useEffect } from "react";
import { Card, CardHeader, CardBody, CardTitle, Row, Col, Button } from "reactstrap";
import axios from "axios";

function Icons() {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [Tags, setTags] = useState([]);
  const [query, setQuery] = useState("");
  const [searchedTags, setSearchedTags] = useState([]);
  const [selectedTags, setSelectedTags] = useState([]);
  const [inputQuery, setInputQuery] = useState("");

  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth() + 1;
  const date = now.getDate();
  const currentTime = year + '-' + month.toString().padStart(2, '0') + '-' + date.toString().padStart(2, '0');

  const fetchTags = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/tags/');
      setTags(response.data);
      setSearchedTags(response.data); // Set the initial searched tags to the fetched tags
    } catch (error) {
      console.error("Failed to fetch tags:", error);
    }
  };

  useEffect(() => {
    fetchTags();
  }, []);

  const handleStartDateChange = (event) => {
    const selectedStartDate = event.target.value + 'T00:00:00';
    if (selectedStartDate && currentTime < selectedStartDate) {
      setStartDate(event.target.value);
    } else {
      setStartDate('');
      alert('Please enter a valid date.');
    }
  };

  const handleEndDateChange = (event) => {
    const selectedEndDate = event.target.value;
    if (startDate && selectedEndDate && startDate <= selectedEndDate) {
      setEndDate(selectedEndDate);
    } else {
      setEndDate('');
      alert('Please enter a valid date.');
    }
  };

  const handleSubmit = async (event) => {
    const tagIds = selectedTags.map(item => item.tag_id);
    localStorage.setItem('start_date', startDate);
    localStorage.setItem('end_date', endDate);
    localStorage.setItem('selected_tags', JSON.stringify(tagIds));
    window.location.href = 'http://localhost:3000/admin/plans';
  };

  const handlequerySubmit = async (event) => {
    localStorage.setItem('start_date', startDate);
    localStorage.setItem('end_date', endDate);
    localStorage.setItem('input_query', inputQuery);
    console.log(inputQuery)
    window.location.href = 'http://localhost:3000/admin/plans';
  };

  const handleSearch = () => {
    let filteredTags = Tags;

    if (!query) {
      setSearchedTags(Tags);
    }

    if (query) {
      filteredTags = filteredTags.filter(({ tag_name }) =>
        tag_name.toLowerCase().includes(query.toLowerCase())
      );
    }

    setSearchedTags(filteredTags);
  };

  const handleSameDate = () => {
    if (startDate) {
      setEndDate(startDate);
    }
  };

  const handleTagClick = (tag) => {
    const selectedTagCount = selectedTags.length;
    const maxTagCount = 10;

    if (selectedTagCount >= maxTagCount) {
      alert(`You can select up to ${maxTagCount} tags.`);
      return;
    }

    if (selectedTags.find(item => item.tag_id === tag.tag_id)) {
      setSelectedTags(selectedTags.filter(item => item.tag_id !== tag.tag_id));
    } else {
      setSelectedTags([...selectedTags, tag]);
    }
  };

  useEffect(() => {
    setSearchedTags(Tags);
  }, [Tags]);

  return (
    <>
      <div className="content">
        <Row>
          <Col md="12">
            <Card className="demo-icons">
              <CardHeader>
                <CardTitle tag="h5">Input for Trip </CardTitle>
              </CardHeader>
              <hr/>
              <CardBody className="all-icons">
                <br/>
                <div id="icons-wrapper">
                  <section>
                    <div>
                      <Col className="ml-auto mr-auto" lg="8">
                        <div>
                          <label htmlFor="startDate">Start Date:</label>
                          <input
                            type="date"
                            id="startDate"
                            value={startDate}
                            onChange={handleStartDateChange}
                          />
                        </div>
                        <br/>
                        <div>
                          <label htmlFor="endDate">End Date:</label>
                          <input
                            type="date"
                            id="endDate"
                            value={endDate}
                            onChange={handleEndDateChange}
                          />
                          <button onClick={handleSameDate}>Daytrip</button>
                        </div>
                        <br/>
                        <hr/>
                        <br/>
                        <h5>Select Your Tags</h5>
                        <div>
                          <input
                            type="search"
                            placeholder="Search for travel tags"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                          />
                          <button onClick={handleSearch}>Search</button>
                        </div>
                        <br/>
                        <div style={{ maxHeight: '240px', overflowY: 'auto' }}>
                          <table className="table table-hover">
                            <thead>
                              <tr className="text-center">
                                <th>Name</th>
                                <th>Action</th>
                              </tr>
                            </thead>
                            <tbody>
                              {searchedTags.map(tag => (
                                <tr className="text-center" key={tag.tag_id}>
                                  <td>{tag.tag_name}</td>
                                  <td>
                                    <Button
                                      className="btn-round"
                                      color="info"
                                      onClick={() => handleTagClick(tag)}
                                    >
                                      Add
                                    </Button>
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                        <br/>
                        <hr/>
                        <br/>
                        <h5>Selected Tags</h5>
                        <div style={{ maxHeight: '240px', overflowY: 'auto' }}>
                          <table className="table table-hover">
                            <thead className="thead-fixed">
                              <tr className="text-center">
                                <th>Name</th>
                                <th>Action</th>
                              </tr>
                            </thead>
                            <tbody>
                              {selectedTags.map(tag => (
                                <tr className="text-center" key={tag.tag_id}>
                                  <td>{tag.tag_name}</td>
                                  <td>
                                    <Button
                                      className="btn-round"
                                      color="danger"
                                      onClick={() => handleTagClick(tag)}
                                      style={{ cursor: 'pointer' }}
                                    >
                                      Delete
                                    </Button>
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                        <br/>
                        <hr/>
                        <br/>
                        <div>
                        <label htmlFor="queryfield">By Query: </label>
                          <input
                            type="search"
                            id="queryfield"
                            placeholder="Input your query for trip"
                            value={inputQuery}
                            onChange={(e) => setInputQuery(e.target.value)}
                          />
                          <button onClick={handlequerySubmit}>Submit</button>
                        </div>
                        <br/>
                        <br/>
                      </Col>
                    </div>
                  </section>
                </div>
              </CardBody>
              <hr/>
              <br/>
              <Col className="ml-auto mr-auto" lg="8">
                          <Row>
                            <Col md="4">
                              <Button 
                                block
                                className="btn-round" 
                                color="primary"
                                href="http://localhost:3000/admin/icons">
                                Reset
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
                                onClick={handleSubmit}
                                
                                >
                                Submit
                              </Button>
                            </Col>
                          </Row>
                        </Col>

            </Card>
          </Col>
        </Row>
      </div>
    </>
  );
}

export default Icons;

