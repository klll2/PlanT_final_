import React from 'react';
import { Button } from 'reactstrap';

const getRandomColor = () => {
  const colors = ["primary", "success", "danger", "warning", "info"];
  const randomIndex = Math.floor(Math.random() * colors.length);
  return colors[randomIndex];
};

const PlanDetails = ({ plcNames, plcTimes}) => {

  return (
    <>
    
      <hr />
      <div className="text-center">
        {plcNames.map((place, index) => (
          <div key={index}>
            <Button color={getRandomColor()} fade={false}>
              <span>{place}</span>
            </Button>
            <br />
            {index < plcTimes.length / 2 && (
              <Button color="secondary" disabled>
                <span> {plcTimes[2 * index]} </span>
                <span> ~  </span>
                <span> {plcTimes[2 * index + 1]} </span>
              </Button>
            )}
            <br />
          </div>
        ))}
      </div>
      <hr />
    </>
  );
};

export default PlanDetails;
