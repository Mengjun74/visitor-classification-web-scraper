import React, { useState } from 'react';

const Questionnaire = ({ data }) => {
  const [responses, setResponses] = useState({});

  const handleResponseChange = (question, choice) => {
    setResponses((prev) => ({
      ...prev,
      [question]: choice,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('User Input:', responses);
  };

  return (
    <div>
      <h1>Title: {data.title}</h1>
      <h2>NLP Classification: {data.classification}</h2>
      <h2>GPT Classification: {data.gpt_classification}</h2>

      <h3>Multiple Choice Questions:</h3>
      <form onSubmit={handleSubmit}>
        {data.multi_choice_questions.map((item, index) => (
          <div key={index}>
            <p>{item.question}</p>
            {item.options.map((option, i) => (
              <label key={i}>
                <input
                  type="radio"
                  name={item.question}
                  value={option}
                  onChange={() => handleResponseChange(item.question, option)}
                  required
                />
                {option}
              </label>
            ))}
          </div>
        ))}

        <h3>General Questions:</h3>
        {data.general_questions.map((item, index) => (
          <div key={index}>
            {item.question.split('\n').map((question, i) => (
              <div key={i}>
                <p>{question.trim()}</p>
                <input
                  type="text"
                  placeholder="Your answer"
                  onChange={(event) => handleResponseChange(`General Question ${i + 1}`, event.target.value)}
                />
              </div>
            ))}
          </div>
        ))}
        <button type="submit">Submit Responses</button>
      </form>
    </div>
  );
};

export default Questionnaire;
