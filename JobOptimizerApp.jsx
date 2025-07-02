
import React, { useState } from 'react';
import axios from 'axios';

export default function JobOptimizerApp() {
  const [jobUrl, setJobUrl] = useState('');
  const [jobText, setJobText] = useState('');
  const [skills, setSkills] = useState([]);
  const [wordCount, setWordCount] = useState(0);
  const [resume, setResume] = useState(null);
  const [optimizedResume, setOptimizedResume] = useState('');
  const [coverLetter, setCoverLetter] = useState('');
  const [interviewQuestions, setInterviewQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const backendURL = 'http://localhost:8000'; // Change to deployed URL if needed

  const handleJobAnalyze = async () => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('job_url', jobUrl);

      const response = await axios.post(`${backendURL}/analyze-job`, formData);
      setJobText(response.data.raw_text);
      setSkills(response.data.skills);
      setWordCount(response.data.word_count);
    } catch (err) {
      setError('Job Analysis Failed: ' + err.response?.data?.detail);
    } finally {
      setLoading(false);
    }
  };

  const handleResumeOptimize = async () => {
    if (!resume || !jobText) {
      setError('Upload resume and analyze job first');
      return;
    }
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('user_resume', resume);
      formData.append('job_text', jobText);

      const response = await axios.post(`${backendURL}/optimize-resume`, formData);
      setOptimizedResume(response.data.optimized_resume);
    } catch (err) {
      setError('Resume Optimization Failed: ' + err.response?.data?.detail);
    } finally {
      setLoading(false);
    }
  };

  const handleCoverLetter = async () => {
    if (!resume || !jobText) {
      setError('Upload resume and analyze job first');
      return;
    }
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('user_resume', resume);
      formData.append('job_text', jobText);

      const response = await axios.post(`${backendURL}/generate-cover-letter`, formData);
      setCoverLetter(response.data.cover_letter);
    } catch (err) {
      setError('Cover Letter Generation Failed: ' + err.response?.data?.detail);
    } finally {
      setLoading(false);
    }
  };

  const handleInterviewPrep = async () => {
    if (!jobText) {
      setError('Analyze a job first');
      return;
    }
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('job_text', jobText);

      const response = await axios.post(`${backendURL}/interview-prep`, formData);
      setInterviewQuestions(response.data.questions);
    } catch (err) {
      setError('Interview Prep Failed: ' + err.response?.data?.detail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h2>🧠 Intelligent Job Application Optimizer</h2>

      <div>
        <input
          type="text"
          placeholder="Enter Job URL"
          value={jobUrl}
          onChange={(e) => setJobUrl(e.target.value)}
          style={{ width: '60%', marginRight: '10px' }}
        />
        <button onClick={handleJobAnalyze}>Analyze Job</button>
      </div>

      <br />

      <div>
        <label>Upload Resume (PDF or DOC): </label>
        <input type="file" onChange={(e) => setResume(e.target.files[0])} />
      </div>

      <br />

      <button onClick={handleResumeOptimize}>Optimize Resume</button>
      <button onClick={handleCoverLetter} style={{ marginLeft: '10px' }}>
        Generate Cover Letter
      </button>
      <button onClick={handleInterviewPrep} style={{ marginLeft: '10px' }}>
        Prepare for Interview
      </button>

      <br /><br />

      {error && <p style={{ color: 'red' }}>{error}</p>}
      {loading && <p>Loading...</p>}

      {jobText && (
        <div>
          <h3>📄 Job Description (Top Words)</h3>
          <p><strong>Word Count:</strong> {wordCount}</p>
          <p><strong>Skills Detected:</strong> {skills.join(', ')}</p>
          <textarea rows="5" value={jobText} readOnly style={{ width: '100%' }} />
        </div>
      )}

      {optimizedResume && (
        <div>
          <h3>✅ Optimized Resume</h3>
          <textarea rows="10" value={optimizedResume} readOnly style={{ width: '100%' }} />
        </div>
      )}

      {coverLetter && (
        <div>
          <h3>✉️ Cover Letter</h3>
          <textarea rows="10" value={coverLetter} readOnly style={{ width: '100%' }} />
        </div>
      )}

      {interviewQuestions.length > 0 && (
        <div>
          <h3>🗣️ Interview Questions</h3>
          <ul>
            {interviewQuestions.map((q, index) => (
              <li key={index}>{q}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
