import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import './style.css';

const API = 'https://nexus-776h.onrender.com';

function App() {
  const [files, setFiles] = useState([]);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState([]);
  const [status, setStatus] = useState('System ready.');
  const [busy, setBusy] = useState(false);

  // Add selected files without removing previously selected files
  function addFiles(newFiles) {
    const pdfFiles = Array.from(newFiles).filter(
      (file) =>
        file.type === 'application/pdf' ||
        file.name.toLowerCase().endsWith('.pdf')
    );

    setFiles((currentFiles) => {
      const existingNames = new Set(
        currentFiles.map((file) => file.name + file.size)
      );

      const newUniqueFiles = pdfFiles.filter(
        (file) => !existingNames.has(file.name + file.size)
      );

      return [...currentFiles, ...newUniqueFiles];
    });
  }

  // File picker
  function handleFileChange(e) {
    addFiles(e.target.files);

    // Reset input so the same file can be selected again if needed
    e.target.value = '';
  }

  // Drag and drop
  function handleDrop(e) {
    e.preventDefault();
    addFiles(e.dataTransfer.files);
  }

  function handleDragOver(e) {
    e.preventDefault();
  }

  // Remove one file
  function removeFile(index) {
    setFiles((currentFiles) =>
      currentFiles.filter((_, i) => i !== index)
    );
  }

  // Clear all files
  function clearFiles() {
    setFiles([]);
  }

  // Upload multiple PDFs
  async function upload() {
    if (!files.length) return;

    setBusy(true);
    setStatus('Indexing documents...');

    const formData = new FormData();

    files.forEach((file) => {
      formData.append('files', file);
    });

    try {
      const response = await fetch(`${API}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.status}`);
      }

      const data = await response.json();

      setStatus(
        `Added ${data.added?.length || 0} file(s), ` +
        `skipped ${data.skipped?.length || 0}, ` +
        `errors ${data.errors?.length || 0}.`
      );
    } catch (error) {
      console.error(error);
      setStatus('Could not upload documents. Check the backend.');
    } finally {
      setBusy(false);
    }
  }

  // Ask question
  async function ask() {
    if (!question.trim()) return;

    setBusy(true);
    setStatus('Searching knowledge base...');

    try {
      const response = await fetch(`${API}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: question.trim(),
        }),
      });

      if (!response.ok) {
        throw new Error(`Query failed: ${response.status}`);
      }

      const data = await response.json();

      setAnswer(data.answer || '');
      setSources(data.sources || []);
      setStatus('Response generated.');
    } catch (error) {
      console.error(error);
      setStatus('Could not reach NEXUS backend.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="app">

      {/* HEADER */}
      <header>
        <div className="brand">
          <span className="orb">✦</span>

          <div>
            <h1>NEXUS</h1>
            <p>Neural Extraction & Unified Search</p>
          </div>
        </div>

        <span className="live">● LOCAL SYSTEM</span>
      </header>

      <main>

        {/* HERO */}
        <section className="hero">
          <p className="eyebrow">
            DOCUMENT INTELLIGENCE / RAG CORE
          </p>

          <h2>
            Your knowledge.
            <br />
            <span>Connected.</span>
          </h2>

          <p className="sub">
            Upload PDFs, search across documents, and receive grounded
            answers with page-level sources.
          </p>
        </section>

        {/* UPLOAD */}
        <section className="panel">

          <div className="panel-title">
            <h3>01 / INGEST DOCUMENTS</h3>
            <span>MAX 50 PDFs</span>
          </div>

          <label
            className="drop"
            onDrop={handleDrop}
            onDragOver={handleDragOver}
          >
            <input
              type="file"
              accept=".pdf,application/pdf"
              multiple
              onChange={handleFileChange}
            />

            <strong>
              Drop PDFs here or choose files
            </strong>

            <small>
              {files.length > 0
                ? `${files.length} PDF(s) selected`
                : 'PDF text extraction · duplicate detection'}
            </small>
          </label>

          {/* SELECTED FILES */}
          {files.length > 0 && (
            <div className="file-list">

              <div className="file-list-header">
                <strong>
                  Selected documents ({files.length})
                </strong>

                <button
                  type="button"
                  onClick={clearFiles}
                  disabled={busy}
                >
                  Clear all
                </button>
              </div>

              {files.map((file, index) => (
                <div
                  className="file-item"
                  key={`${file.name}-${file.size}-${index}`}
                >
                  <span>📄</span>

                  <span className="file-name">
                    {file.name}
                  </span>

                  <button
                    type="button"
                    onClick={() => removeFile(index)}
                    disabled={busy}
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>
          )}

          <button
            onClick={upload}
            disabled={busy || !files.length}
          >
            {busy
              ? 'INDEXING...'
              : 'INITIALIZE INDEXING ↗'}
          </button>

        </section>

        {/* QUERY */}
        <section className="panel">

          <div className="panel-title">
            <h3>02 / QUERY NEXUS</h3>
            <span>TOP-K SEMANTIC SEARCH</span>
          </div>

          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask anything about your uploaded documents..."
          />

          <button
            onClick={ask}
            disabled={busy || !question.trim()}
          >
            {busy
              ? 'SEARCHING...'
              : 'RUN QUERY ↗'}
          </button>

          {/* ANSWER */}
          {answer && (
            <div className="answer">

              <h4>RESPONSE</h4>

              <p>{answer}</p>

              {sources.length > 0 && (
                <>
                  <h4>SOURCES</h4>

                  <ul>
                    {sources.map((source, index) => (
                      <li key={index}>
                        {source.filename}
                        {' · '}
                        page {source.page}
                        {' · '}
                        relevance {source.score}
                      </li>
                    ))}
                  </ul>
                </>
              )}

            </div>
          )}

        </section>

        {/* STATUS */}
        <div className="status">
          {busy ? '◌ ' : '✓ '}
          {status}
        </div>

      </main>
    </div>
  );
}

createRoot(
  document.getElementById('root')
).render(
  <App />
);