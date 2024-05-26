import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import './App.css';
import articlesData from './240301_240310_all_cats_arxiv_metadata.json';
import Latex from 'react-latex-next';
import Login from './Login'; // Import the Login component
import SignUp from './SignUp'; // Import the SignUp component
import UserInfo from './UserInfo'; // Import the UserInfo component

const JargonDefinitions = ({ terms }) => (
  <div className="jargon-definitions">
    <h3>Jargon Terms</h3>
    <ul>
      {terms.map((term, index) => (
        <li key={index}>
          <strong>{term.word}:</strong> {term.definition}
        </li>
      ))}
    </ul>
  </div>
);

const Article = ({ title, author, date, link, summary, terms }) => (
  <div className="article">
    <h2>
      <a href={link} target="_blank" rel="noopener noreferrer">
        {title}
      </a>
    </h2>
    <p className="author-date">By {author} on {new Date(date).toLocaleDateString()}</p>
    <Latex>{summary}</Latex>
    <JargonDefinitions terms={terms} />
    <div className="article-footer">
      <a href={link} target="_blank" rel="noopener noreferrer">Read more</a>
    </div>
  </div>
);

function MainPage({ articles, searchQuery, setSearchQuery, handleSearch, filteredArticles }) {
  const navigate = useNavigate();

  return (
    <>
      <div className="search-bar">
        <input
          type="text"
          placeholder="Search..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button type="button" onClick={handleSearch}>Submit</button>
        <button
          type="button"
          className="login-button"
          onClick={() => navigate('/login')}
        >
          Login
        </button>
      </div>
      <main>
        {filteredArticles.map(article => (
          <Article key={article.id} {...article} />
        ))}
      </main>
    </>
  );
}

function App() {
  const [articles, setArticles] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredArticles, setFilteredArticles] = useState([]);

  useEffect(() => {
    const articles = Object.values(articlesData).map((article, index) => ({
      id: index + 1,
      title: article.title,
      author: article.authors.join(', '),
      date: article.updated,
      link: article.url,
      summary: article.summary,
      categories: article.categories,
      comments: article.comments,
      terms: extractJargonTerms(article.summary), // Function to extract jargon terms
    }));
    setArticles(articles);
    setFilteredArticles(articles);
  }, []);

  const extractJargonTerms = (summary) => {
    // Example function to extract jargon terms
    // In a real application, you might use an API or a dictionary
    const terms = [
      { word: 'Graph', definition: 'A structure amounting to a set of objects in which some pairs of the objects are in some sense "related".' },
      { word: 'Algorithm', definition: 'A process or set of rules to be followed in calculations or other problem-solving operations.' },
      // Add more terms as needed
    ];
    return terms;
  };

  const handleSearch = () => {
    const query = searchQuery.toLowerCase();
    const filtered = articles.filter(article =>
      article.title.toLowerCase().includes(query) ||
      article.author.toLowerCase().includes(query) ||
      article.summary.toLowerCase().includes(query)
    );
    setFilteredArticles(filtered);
  };

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Science Dejargonizer</h1>
        </header>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/userinfo" element={<UserInfo />} />
          <Route path="/" element={
            <MainPage
              articles={articles}
              searchQuery={searchQuery}
              setSearchQuery={setSearchQuery}
              handleSearch={handleSearch}
              filteredArticles={filteredArticles}
            />
          } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
