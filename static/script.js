const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (event) => {
  if (event.key === 'Enter') {
    sendMessage();
  }
});

function sendMessage() {
  const message = userInput.value;
  userInput.value = '';
  appendMessage('user', message);

  fetch('/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `message=${encodeURIComponent(message)}`
  })
      .then(response => {
        if (!response.ok) {
          console.error("Ошибка HTTP:", response.status); // Логирование ошибки HTTP
          throw new Error("Ошибка сети");
        }
        return response.json();
      })
    .then(data => {
      console.log("Данные от сервера:", data); // Логирование данных от сервера
      appendMessage('kurt', data.response);
    })
    .catch(error => {
      console.error("Ошибка при отправке сообщения:", error);
      appendMessage('kurt', "Что-то пошло не так. Попробуй ещё раз."); // Добавлено сообщение об ошибке
    });
}

function appendMessage(sender, message) {
  const messageElement = document.createElement('div');
  messageElement.classList.add('message', sender === 'user' ? 'user-message' : 'kurt-message');

  const messageContent = document.createElement('p');
  messageContent.textContent = message;

  messageElement.appendChild(messageContent);
  chatHistory.appendChild(messageElement);

  // Прокрутка вниз
  chatHistory.scrollTop = chatHistory.scrollHeight;
}
// ... (остальной код JavaScript)

const clearHistoryButton = document.getElementById('clear-history');
clearHistoryButton.addEventListener('click', clearHistory);

function clearHistory() {
    // Очищаем историю на стороне клиента
    chatHistory.innerHTML = '';

    // Отправляем запрос на сервер, чтобы очистить историю сессии
    fetch('/clear-history', {
        method: 'POST'
    })
    .catch(error => {
        console.error("Ошибка при очистке истории:", error);
    });
}
