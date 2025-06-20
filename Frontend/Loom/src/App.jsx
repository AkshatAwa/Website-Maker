import { useState } from 'react'

function App() {
  const [prompt, setPrompt] = useState('')
  const [generatedHtml, setGeneratedHtml] = useState('')

  const handlePromptChange = (e) => setPrompt(e.target.value)

  const handleGenerate = async () => {
    try {
      const res = await fetch('http://127.0.0.1:5000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      })

      const data = await res.json()

      if (res.ok) {
        setGeneratedHtml(data.html)
      } else {
        console.error(data.error || 'Generation error')
      }
    } catch (err) {
      console.error('Error:', err)
    }
  }

  return (
    <div style={{ padding: '2rem' }}>
      <h1>AI Webpage Generator</h1>
      <textarea
        rows={4}
        cols={80}
        placeholder="Describe your website: 'Portfolio with 3 cards and a navbar'"
        value={prompt}
        onChange={handlePromptChange}
      />
      <br />
      <button onClick={handleGenerate}>Generate</button>

      <h2>Live Preview</h2>
      <iframe
        srcDoc={generatedHtml}
        width="100%"
        height="500"
        title="Generated HTML"
        sandbox="allow-scripts"
      />
    </div>
  )
}

export default App
