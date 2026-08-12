const GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"; // Placeholder for the actual API key
const GEMINI_MODEL = "gemini-1.5-flash";

document.addEventListener('DOMContentLoaded', () => {
  const chatInput = document.getElementById('chat-input');
  const chatBtn = document.getElementById('chat-btn');
  const chatBox = document.getElementById('chat-box');
  const typingIndicator = document.getElementById('typing-indicator');
  
  let indiaData = null;

  // Pre-fetch the data to use as context
  fetch('data/explorer.json')
    .then(response => response.json())
    .then(data => {
      indiaData = data;
      console.log("IndiaMetrix data loaded for AI context.");
    })
    .catch(err => console.error("Failed to load data context:", err));

  const appendMessage = (text, sender) => {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    msgDiv.textContent = text;
    
    // Insert before typing indicator
    chatBox.insertBefore(msgDiv, typingIndicator);
    chatBox.scrollTop = chatBox.scrollHeight;
  };

  const handleSend = async () => {
    const userText = chatInput.value.trim();
    if (!userText) return;

    if (GEMINI_API_KEY === "YOUR_GEMINI_API_KEY_HERE") {
      appendMessage(userText, 'user');
      chatInput.value = '';
      setTimeout(() => {
        appendMessage("System Error: API Key not configured. Please add your Gemini API Key in assets/js/ask.js.", 'error');
      }, 500);
      return;
    }

    if (!indiaData) {
      appendMessage("System Error: Data not loaded yet. Please wait a moment.", 'error');
      return;
    }

    // Append user message
    appendMessage(userText, 'user');
    chatInput.value = '';
    chatBtn.disabled = true;
    chatInput.disabled = true;
    typingIndicator.style.display = 'block';
    chatBox.scrollTop = chatBox.scrollHeight;

    // Prepare System Prompt
    const systemInstruction = `
      You are the official IndiaMetrix AI Assistant. 
      Your ONLY purpose is to answer questions about Indian demographics, economy, and statistics using the provided JSON dataset.
      
      RULES:
      1. ONLY use the data provided in this prompt. Do not use outside knowledge.
      2. If a user asks a question that cannot be answered with the provided data (e.g. "Who is the PM?", "How to cook?"), you MUST refuse to answer and remind them you are a data assistant.
      3. Keep answers concise, factual, and easy to read.
      
      DATABASE CONTENT:
      ${JSON.stringify(indiaData).substring(0, 15000)} // Truncate if necessary, though explorer.json is relatively small
    `;

    try {
      const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${GEMINI_API_KEY}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          systemInstruction: {
            parts: [{ text: systemInstruction }]
          },
          contents: [{
            role: "user",
            parts: [{ text: userText }]
          }],
          generationConfig: {
            temperature: 0.1
          }
        })
      });

      const data = await response.json();
      
      typingIndicator.style.display = 'none';
      
      if (data.error) {
        appendMessage(`API Error: ${data.error.message}`, 'error');
      } else if (data.candidates && data.candidates.length > 0) {
        const botResponse = data.candidates[0].content.parts[0].text;
        appendMessage(botResponse, 'bot');
      } else {
        appendMessage("Received an empty response.", 'error');
      }

    } catch (err) {
      typingIndicator.style.display = 'none';
      appendMessage(`Network Error: ${err.message}`, 'error');
    } finally {
      chatBtn.disabled = false;
      chatInput.disabled = false;
      chatInput.focus();
    }
  };

  chatBtn.addEventListener('click', handleSend);
  chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSend();
  });
});
