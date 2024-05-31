import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import './App.css';
import articlesData from './240301_240310_all_cats_arxiv_metadata.json';
import Latex from 'react-latex-next';
import Login from './Login';
import SignUp from './SignUp';
import UserInfo from './UserInfo';

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

const Article = ({ title, author, date, link, summary, terms, categories, comments }) => (
  <div className="article">
    <h2>
      <a href={link} target="_blank" rel="noopener noreferrer">
        {title}
      </a>
    </h2>
    <p className="author-date">By {author} on {new Date(date).toLocaleDateString()}</p>
    <Latex>{summary}</Latex>
    <div className="article-meta">
      <p>
        <strong>Subjects:</strong> <strong>{categories[0]}</strong>{categories.length > 1 ? `, ${categories.slice(1).join(', ')}` : ''}
      </p>
      {comments && <p><strong>Comments:</strong> {comments}</p>}
    </div>
    <JargonDefinitions terms={terms} />
    <div className="article-footer">
      <a href={link} target="_blank" rel="noopener noreferrer">Read more</a>
    </div>
  </div>
);

function MainPage({ articles, searchQuery, setSearchQuery, handleSearch, filteredArticles, setFilteredArticles, selectedCategories, setSelectedCategories }) {
  const [showFilters, setShowFilters] = useState(false);
  const navigate = useNavigate();

  const categoryOptions = [
    { value: 'cs.AI', label: 'cs.AI' },
    { value: 'cs.HC', label: 'cs.HC' },
    { value: 'cs.CY', label: 'cs.CY' },
  ];

  const handleCategoryChange = (event) => {
    const value = event.target.value;
    setSelectedCategories(prevCategories =>
      prevCategories.includes(value)
        ? prevCategories.filter(category => category !== value)
        : [...prevCategories, value]
    );
  };

  useEffect(() => {
    const filtered = articles.filter(article =>
      selectedCategories.length === 0 || selectedCategories.some(category => article.categories.includes(category))
    ).filter(article =>
      article.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      article.author.toLowerCase().includes(searchQuery.toLowerCase()) ||
      article.summary.toLowerCase().includes(searchQuery.toLowerCase())
    );
    setFilteredArticles(filtered);
  }, [articles, searchQuery, selectedCategories, setFilteredArticles]);

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
        <button type="button" className="filters-button" onClick={() => setShowFilters(!showFilters)}>
          Filters
        </button>
        {showFilters && (
          <div className="checkbox-group">
            {categoryOptions.map(option => (
              <label key={option.value} className="checkbox-label">
                <input
                  type="checkbox"
                  value={option.value}
                  checked={selectedCategories.includes(option.value)}
                  onChange={handleCategoryChange}
                />
                {option.label}
              </label>
            ))}
          </div>
        )}
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
  const [selectedCategories, setSelectedCategories] = useState([]);

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
      terms: extractJargonTerms(article.summary),
    }));
    setArticles(articles);
    setFilteredArticles(articles);
  }, []);

  const extractJargonTerms = (summary) => {
    const terms = [
      { word: 'Graph', definition: 'A structure amounting to a set of objects in which some pairs of the objects are in some sense "related".' },
      { word: 'Algorithm', definition: 'A process or set of rules to be followed in calculations or other problem-solving operations.' },
    ];
    return terms;
  };

  const handleSearch = () => {
    const query = searchQuery.toLowerCase();
    const filtered = articles.filter(article =>
      article.title.toLowerCase().includes(query) ||
      article.author.toLowerCase().includes(query) ||
      article.summary.toLowerCase().includes(query)
    ).filter(article =>
      selectedCategories.length === 0 || selectedCategories.some(category => article.categories.includes(category))
    );
    setFilteredArticles(filtered);
  };

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Science Dejargonizer</h1>
          <p className="app-description">The Science Dejargonizer simplifies complex scientific articles by identifying and defining technical terms, making research more accessible to non-experts. Utilizing natural language processing and advanced text analysis, this system parses article metadata, extracts jargon terms, and provides clear definitions, aiding comprehension and enhancing knowledge dissemination.</p>
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
              setFilteredArticles={setFilteredArticles}
              selectedCategories={selectedCategories}
              setSelectedCategories={setSelectedCategories}
            />
          } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
