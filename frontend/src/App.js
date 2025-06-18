import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState('');
  const [location, setLocation] = useState('');
  const [jobs, setJobs] = useState([]);
  const [walkinJobs, setWalkinJobs] = useState([]);
  const [baseResume, setBaseResume] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [optimizedResume, setOptimizedResume] = useState(null);
  const [companyName, setCompanyName] = useState('');
  const [jobTitle, setJobTitle] = useState('');
  const [pdfPath, setPdfPath] = useState('');

  const backendUrl = 'http://localhost:8000';

  const searchJobs = async () => {
    try {
      const res = await axios.get(`${backendUrl}/search_jobs/`, {
        params: { query, location }
      });
      setJobs(res.data);
    } catch (error) {
      alert('Error fetching jobs');
    }
  };

  const searchWalkinJobs = async () => {
    try {
      const res = await axios.get(`${backendUrl}/walkin_jobs/`, {
        params: { query, location }
      });
      setWalkinJobs(res.data);
    } catch (error) {
      alert('Error fetching walk-in jobs');
    }
  };

  const optimizeResume = async () => {
    try {
      const baseResumeObj = JSON.parse(baseResume);
      const res = await axios.post(`${backendUrl}/optimize_resume/`, {
        base_resume: baseResumeObj,
        job_description: jobDescription
      });
      setOptimizedResume(res.data);
    } catch (error) {
      alert('Error optimizing resume. Ensure base resume is valid JSON.');
    }
  };

  const generatePdf = async () => {
    try {
      const baseResumeObj = JSON.parse(baseResume);
      const res = await axios.post(`${backendUrl}/generate_pdf/`, {
        base_resume: baseResumeObj,
        company_name: companyName,
        job_title: jobTitle
      });
      setPdfPath(res.data.pdf_path);
    } catch (error) {
      alert('Error generating PDF. Ensure inputs are valid.');
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Auto Job Application Chatbot Frontend</h1>

      <section>
        <h2>Job Search</h2>
        <input placeholder="Job Query" value={query} onChange={e => setQuery(e.target.value)} />
        <input placeholder="Location" value={location} onChange={e => setLocation(e.target.value)} />
        <button onClick={searchJobs}>Search Jobs</button>
        <button onClick={searchWalkinJobs}>Search Walk-in Jobs</button>

        <h3>Jobs</h3>
        <ul>
          {jobs.map(job => (
            <li key={job.id}>{job.title} at {job.company} - {job.location}</li>
          ))}
        </ul>

        <h3>Walk-in Jobs</h3>
        <ul>
          {walkinJobs.map(job => (
            <li key={job.id}>{job.title} at {job.company} - {job.location}</li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Resume Optimization</h2>
        <textarea
          rows={10}
          cols={50}
          placeholder='Base Resume JSON'
          value={baseResume}
          onChange={e => setBaseResume(e.target.value)}
        />
        <br />
        <textarea
          rows={5}
          cols={50}
          placeholder='Job Description'
          value={jobDescription}
          onChange={e => setJobDescription(e.target.value)}
        />
        <br />
        <button onClick={optimizeResume}>Optimize Resume</button>

        {optimizedResume && (
          <pre>{JSON.stringify(optimizedResume, null, 2)}</pre>
        )}
      </section>

      <section>
        <h2>Generate PDF Resume</h2>
        <input
          placeholder="Company Name"
          value={companyName}
          onChange={e => setCompanyName(e.target.value)}
        />
        <input
          placeholder="Job Title"
          value={jobTitle}
          onChange={e => setJobTitle(e.target.value)}
        />
        <br />
        <button onClick={generatePdf}>Generate PDF</button>

        {pdfPath && (
          <p>PDF generated at: {pdfPath}</p>
        )}
      </section>
    </div>
  );
}

export default App;
