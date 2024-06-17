import React, { useState, useEffect } from "react";
import axios from "axios";

function MyForm() {
  const [options, setOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState(""); // 선택된 옵션을 저장할 상태
  const [result, setResult] = useState('no');
  const [result2, setResult2] = useState('no');
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/send/')
      .then(response => {
        setOptions(response.data);
      })
      .catch(error => {
        console.error('Error fetching options:', error);
      });
  }, []);

  const handleSubmit = (e) => {

    // 선택된 옵션을 백엔드로 보내는 API 호출
    axios.post('http://127.0.0.1:8000/api/recieve/', {ops : selectedOption})
      .then(response => {
        setResult(response.data['1']);
        setResult2(response.data['2']); // 받은 응답에서 이름을 가져와 결과로 설정
      })
      .catch(error => {
        console.error('Error retrieving data:', error);
      });

    e.preventDefault();
    setSubmitted(true); // 폼이 제출되었음을 표시
      
  };

  

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Select an option:
        <select
          value={selectedOption} // 선택된 값을 표시하기 위해 value 속성에 selectedOption 사용
          onChange={(e) => setSelectedOption(e.target.value)} // 셀렉트 박스에서 옵션 선택 시 selectedOption 업데이트
        >
          <option value="">Select an option</option>
          {options.map((option, index) => (
            <option key={index} value={option}>{option}</option>
          ))}
        </select>
      </label>
      <br />
      <button type="submit">Submit</button>
      {submitted && <p>Selected option: {selectedOption}</p>}
      {result && <p>Result: <br/>{result}<br/>{result2}</p>}
    </form>
  );
}

export default MyForm;