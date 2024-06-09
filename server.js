const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const chatbot = require('./public/chatbot'); // Importing chatbot.js module

const app = express();
const port = process.env.PORT || 4100;

app.use(bodyParser.json());

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, 'public')));

// Route to handle sending messages to the chatbot
app.post('/chat', async (req, res) => {
  const userMessage = req.body.message;

  try {
    const result = await chatbot.run(userMessage); // Utilize the run function from chatbot.js
    res.json({ reply: result });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Route to handle default path and serve index.html
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
