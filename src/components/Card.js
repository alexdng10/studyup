// src/components/Card.js

import React from 'react';

function Card({quiz}) {
  return(
    <div className="tc bg-light-green dib br3 pa3 ma2 grow bw2 shadow-5">
      <img className="br-100 h3 w3 dib" alt={quiz.name} src={process.env.PUBLIC_URL + quiz.imgPath} />
      <div>
        <h2>{quiz.name}</h2>
      </div>
    </div>
  );
}

export default Card;