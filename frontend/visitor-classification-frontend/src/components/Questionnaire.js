import React, { useState } from 'react';
import axios from 'axios';

const Questionnaire = ({ data }) => {
  const [responses, setResponses] = useState({});
  const [submitError, setSubmitError] = useState(null);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  const handleResponseChange = (question, choice) => {
    setResponses((prev) => ({
      ...prev,
      [question]: choice,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log('User Responses:', responses);

    const responsePayload = {
      classification: data.classification,
      gpt_classification: data.gpt_classification,
      questions: {
        multi_choice: data.multi_choice_questions, // Use the correct data structure
        general: data.general_questions,
      },
      user_responses: responses, // User's responses
    };

    try {
      const response = await axios.post('/submit-response', responsePayload);
      console.log(response.data);
      setSubmitSuccess(true);
      setSubmitError(null);
    } catch (error) {
      setSubmitError(error.response ? error.response.data.error : 'Something went wrong');
      setSubmitSuccess(false);
    }
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
                  onChange={(event) => handleResponseChange(`General Question ${index + 1}`, event.target.value)}
                />
              </div>
            ))}
          </div>
        ))}

        <button type="submit">Submit Responses</button>
      </form>

      {submitSuccess && <p style={{ color: 'green' }}>Response saved successfully!</p>}
      {submitError && <p style={{ color: 'red' }}>{submitError}</p>}
    </div>
  );
};

export default Questionnaire;
