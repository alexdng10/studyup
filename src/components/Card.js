// src/components/Card.js

import React from 'react';
import './Card.css'; 
function Card({ quiz }) {
  const imageUrl = `${process.env.PUBLIC_URL}/assets/img/his.webp`;
  console.log(quiz); // Log the quiz data
  return (
    <div className="course-card">
      <img className="br-100 h3 w3 dib" alt={quiz.name} src={process.env.PUBLIC_URL + quiz.imgPath} />
      <div>
        <h2>{quiz.name}</h2>
      </div>
    </div>
  );
}

export default Card;