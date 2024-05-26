import React, { useState } from 'react';
import './UserInfo.css';

const UserInfo = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [ratings, setRatings] = useState({
    'cs.hc': 1,
    'cs.ai': 1,
    'cs.cy': 1,
  });

  const handleRatingChange = (topic, value) => {
    setRatings({
      ...ratings,
      [topic]: value,
    });
  };

  const handleSubmit = () => {
    // Handle form submission logic here
    console.log('User Info Submitted', { name, email, ratings });
  };

  return (
    <div className="user-info-container">
      <div className="user-info-box">
        <h2>User Information</h2>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="email"
          placeholder="Short Description"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <div className="topic-rating">
          <label>Rate your knowledge on Human-Computer Interaction (cs.hc):</label>
          <select
            value={ratings['cs.hc']}
            onChange={(e) => handleRatingChange('cs.hc', e.target.value)}
          >
            {[1, 2, 3, 4, 5].map(value => (
              <option key={value} value={value}>{value}</option>
            ))}
          </select>
        </div>
        <div className="topic-rating">
          <label>Rate your knowledge on Artificial Intelligence (cs.ai):</label>
          <select
            value={ratings['cs.ai']}
            onChange={(e) => handleRatingChange('cs.ai', e.target.value)}
          >
            {[1, 2, 3, 4, 5].map(value => (
              <option key={value} value={value}>{value}</option>
            ))}
          </select>
        </div>
        <div className="topic-rating">
          <label>Rate your knowledge on Cybersecurity (cs.cy):</label>
          <select
            value={ratings['cs.cy']}
            onChange={(e) => handleRatingChange('cs.cy', e.target.value)}
          >
            {[1, 2, 3, 4, 5].map(value => (
              <option key={value} value={value}>{value}</option>
            ))}
          </select>
        </div>
        <button type="button" onClick={handleSubmit}>Submit</button>
      </div>
    </div>
  );
};

export default UserInfo;
