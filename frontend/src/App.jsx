import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API = "http://127.0.0.1:8000";

const stages = [
  "Applied",
  "Screening",
  "Interview",
  "Offer",
  "Hired",
];

function App() {
  const [candidates, setCandidates] = useState([]);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [search, setSearch] = useState("");

  const [searchResults, setSearchResults] = useState(null);
  const [searchExplanation, setSearchExplanation] = useState("");
  const [searchError, setSearchError] = useState("");

  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [candidateHistory, setCandidateHistory] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(false);

  const loadCandidates = async () => {
    try {
      const response = await axios.get(`${API}/candidates`);
      setCandidates(response.data);
    } catch (error) {
      console.error("Failed to load candidates:", error);
    }
  };

  useEffect(() => {
    loadCandidates();
  }, []);

  const addCandidate = async (e) => {
    e.preventDefault();

    if (!name.trim() || !email.trim()) {
      alert("Please enter name and email.");
      return;
    }

    try {
      await axios.post(`${API}/candidates`, {
        name,
        email,
      });

      setName("");
      setEmail("");
      setSearch("");
      setSearchResults(null);
      loadCandidates();
    } catch (error) {
      alert("Failed to add candidate.");
    }
  };

  const moveCandidate = async (candidate) => {
    const currentIndex = stages.indexOf(candidate.current_stage);

    if (
      currentIndex === -1 ||
      currentIndex === stages.length - 1
    ) {
      return;
    }

    const nextStage = stages[currentIndex + 1];

    try {
      await axios.post(
        `${API}/candidates/${candidate.id}/move`,
        {
          to_stage: nextStage,
        }
      );

      await loadCandidates();

      if (selectedCandidate?.id === candidate.id) {
        openCandidate(candidate.id);
      }
    } catch (error) {
      alert(
        error.response?.data?.detail ||
          "Unable to move candidate."
      );
    }
  };

  const rejectCandidate = async (candidate) => {
    try {
      await axios.post(
        `${API}/candidates/${candidate.id}/move`,
        {
          to_stage: "Rejected",
        }
      );

      await loadCandidates();

      if (selectedCandidate?.id === candidate.id) {
        openCandidate(candidate.id);
      }
    } catch (error) {
      alert(
        error.response?.data?.detail ||
          "Unable to reject candidate."
      );
    }
  };

  const openCandidate = async (candidateId) => {
    setLoadingHistory(true);

    try {
      const response = await axios.get(
        `${API}/candidates/${candidateId}`
      );

      setSelectedCandidate(response.data.candidate);
      setCandidateHistory(response.data.history);
    } catch (error) {
      console.error("Failed to load candidate:", error);
      alert("Unable to load candidate details.");
    } finally {
      setLoadingHistory(false);
    }
  };

  const closeCandidate = () => {
    setSelectedCandidate(null);
    setCandidateHistory([]);
  };

  const getCurrentStageDuration = () => {
    if (!candidateHistory.length) {
      return "Unknown";
    }

    const latestHistory =
      candidateHistory[candidateHistory.length - 1];

    const startTime = new Date(latestHistory.timestamp);
    const now = new Date();

    const diffMs = Math.max(
      0,
      now.getTime() - startTime.getTime()
    );

    const totalMinutes = Math.floor(
      diffMs / (1000 * 60)
    );

    const days = Math.floor(totalMinutes / 1440);

    const hours = Math.floor(
      (totalMinutes % 1440) / 60
    );

    const minutes = totalMinutes % 60;

    if (days > 0) {
      return `${days}d ${hours}h`;
    }

    if (hours > 0) {
      return `${hours}h ${minutes}m`;
    }

    return `${minutes}m`;
  };

  const handleSearch = async (e) => {
    const value = e.target.value;

    setSearch(value);
    setSearchError("");
    setSearchExplanation("");

    if (!value.trim()) {
      setSearchResults(null);
      return;
    }

    try {
      const response = await axios.get(
        `${API}/search`,
        {
          params: {
            q: value,
          },
        }
      );

      setSearchResults(response.data.results);

      setSearchExplanation(
        response.data.explanation
      );
    } catch (error) {
      setSearchResults([]);

      setSearchError(
        error.response?.data?.detail ||
          "Unable to understand search."
      );
    }
  };

  const displayedCandidates =
    searchResults !== null
      ? searchResults
      : candidates;

  const rejectedCandidates =
    displayedCandidates.filter(
      (candidate) =>
        candidate.current_stage === "Rejected"
    );

  return (
    <div className="app">

      {/* Header */}

      <header className="header">

        <div>
          <h1>Mini Hiring Pipeline</h1>

          <p>
            Manage candidates through the hiring process
          </p>
        </div>

        <input
          className="search"
          type="text"
          placeholder="Try: Find Priya Sharam"
          value={search}
          onChange={handleSearch}
        />

      </header>

      {/* Search feedback */}

      {search && (
        <section className="search-feedback">

          {searchExplanation && (
            <p className="search-explanation">
              {searchExplanation}
            </p>
          )}

          {searchError && (
            <p className="search-error">
              {searchError}
            </p>
          )}

        </section>
      )}

      {/* Add Candidate */}

      <section className="add-section">

        <h2>Add Candidate</h2>

        <form onSubmit={addCandidate}>

          <input
            placeholder="Candidate name"
            value={name}
            onChange={(e) =>
              setName(e.target.value)
            }
          />

          <input
            placeholder="Email"
            type="email"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
          />

          <button type="submit">
            Add Candidate
          </button>

        </form>

      </section>

      {/* Pipeline */}

      <main className="pipeline">

        {/* Normal pipeline stages */}

        {stages.map((stage) => {

          const stageCandidates =
            displayedCandidates.filter(
              (candidate) =>
                candidate.current_stage === stage
            );

          return (
            <div
              className="stage-column"
              key={stage}
            >

              <div className="stage-header">

                <h2>{stage}</h2>

                <span>
                  {stageCandidates.length}
                </span>

              </div>

              {stageCandidates.map(
                (candidate) => (

                  <div
                    className="candidate-card"
                    key={candidate.id}
                    onClick={() =>
                      openCandidate(candidate.id)
                    }
                  >

                    <h3>
                      {candidate.name}
                    </h3>

                    <p>
                      {candidate.email}
                    </p>

                    <div
                      className="actions"
                      onClick={(e) =>
                        e.stopPropagation()
                      }
                    >

                      {stage !== "Hired" && (
                        <button
                          onClick={() =>
                            moveCandidate(candidate)
                          }
                        >
                          Move →
                        </button>
                      )}

                      {stage !== "Hired" && (
                        <button
                          className="reject"
                          onClick={() =>
                            rejectCandidate(candidate)
                          }
                        >
                          Reject
                        </button>
                      )}

                    </div>

                    <small>
                      Click candidate for history
                    </small>

                  </div>
                )
              )}

              {stageCandidates.length === 0 && (
                <div className="empty">
                  No candidates
                </div>
              )}

            </div>
          );
        })}

        {/* Rejected column */}

        <div className="stage-column rejected-column">

          <div className="stage-header">

            <h2>Rejected</h2>

            <span>
              {rejectedCandidates.length}
            </span>

          </div>

          {rejectedCandidates.map(
            (candidate) => (

              <div
                className="candidate-card"
                key={candidate.id}
                onClick={() =>
                  openCandidate(candidate.id)
                }
              >

                <h3>
                  {candidate.name}
                </h3>

                <p>
                  {candidate.email}
                </p>

                <small>
                  Click candidate for history
                </small>

              </div>

            )
          )}

          {rejectedCandidates.length === 0 && (
            <div className="empty">
              No rejected candidates
            </div>
          )}

        </div>

      </main>

      {/* Candidate Details Modal */}

      {selectedCandidate && (

        <div
          className="modal-overlay"
          onClick={closeCandidate}
        >

          <div
            className="candidate-modal"
            onClick={(e) =>
              e.stopPropagation()
            }
          >

            <button
              className="close-button"
              onClick={closeCandidate}
            >
              ×
            </button>

            <h2>
              {selectedCandidate.name}
            </h2>

            <p>
              {selectedCandidate.email}
            </p>

            <div className="current-stage">

              <strong>
                Current Stage
              </strong>

              <span>
                {selectedCandidate.current_stage}
              </span>

            </div>

            <div className="duration">

              <strong>
                Time in Current Stage
              </strong>

              <span>
                {loadingHistory
                  ? "Loading..."
                  : getCurrentStageDuration()}
              </span>

            </div>

            <h3>
              History
            </h3>

            <div className="history">

              {loadingHistory ? (

                <p>
                  Loading history...
                </p>

              ) : candidateHistory.length === 0 ? (

                <p>
                  No history available.
                </p>

              ) : (

                candidateHistory.map(
                  (item, index) => (

                    <div
                      className="history-item"
                      key={item.id}
                    >

                      <div className="history-dot">
                        {index + 1}
                      </div>

                      <div>

                        <strong>
                          {item.from_stage
                            ? `${item.from_stage} → ${item.to_stage}`
                            : item.to_stage}
                        </strong>

                        <p>
                          {new Date(
                            item.timestamp
                          ).toLocaleString()}
                        </p>

                      </div>

                    </div>

                  )
                )

              )}

            </div>

          </div>

        </div>

      )}

    </div>
  );
}

export default App;