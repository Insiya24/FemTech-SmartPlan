document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('send-button');
    if (sendButton) {
      sendButton.addEventListener('click', async () => {
        const userInput = document.getElementById('user-input').value.trim();
        if (!userInput) return;
  
        try {
          const response = await fetch('/chat', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userInput }),
          });
  
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
  
          const data = await response.json();
          const botReply = data.reply;
  
          const messagesContainer = document.getElementById('messages');
  
          // Display user message
          const userMessageElement = document.createElement('div');
          userMessageElement.textContent = `You: ${userInput}`;
          userMessageElement.classList.add('message', 'user');
          messagesContainer.appendChild(userMessageElement);
  
          // Display bot reply
          const botMessageElement = document.createElement('div');
          botMessageElement.textContent = `Bot: ${botReply}`;
          botMessageElement.classList.add('message', 'bot');
          messagesContainer.appendChild(botMessageElement);
  
          // Clear the input field
          document.getElementById('user-input').value = '';
  
          // Scroll to the bottom
          messagesContainer.scrollTop = messagesContainer.scrollHeight;
        } catch (error) {
          console.error('Error:', error.message);
          // Handle error display or other actions as needed
          const errorMessageElement = document.createElement('div');
          errorMessageElement.textContent = 'Sorry, something went wrong. Please try again later.';
          errorMessageElement.classList.add('message', 'error');
          messagesContainer.appendChild(errorMessageElement);
        }
      });
    } else {
      console.error('Element with id "send-button" not found.');
    }
  });
  