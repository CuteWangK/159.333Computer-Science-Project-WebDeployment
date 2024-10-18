<template>
  <div class="chat-container">
    <div class="chat-box">
      <div v-for="(message, index) in messages" :key="index" :class="['message', message.sender === 'You' ? 'user-message' : 'bot-message']">
        <div class="message-content">
          <strong>{{ message.sender }} ({{ formatTimestamp(message.timestamp) }}):</strong>
          <div class="message-text">{{ message.text }}</div>
        </div>
      </div>
    </div>

    <div class="chat-input">
      <input
          v-model="newMessage"
          type="text"
          class="form-control"
          placeholder="Enter your message"
          @keyup.enter="sendMessage"
      />
      <button class="btn btn-success mt-2" @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick, watch } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

export default {
  name: "ChatArea",

  setup() {
    const route = useRoute();
    const uuid = ref(route.params.uuid);
    const messages = ref([]);
    const newMessage = ref("");
    const loading = ref(false);

    const getTimestamp = () => {
      return Math.floor(Date.now() / 1000);
    };

    const formatTimestamp = (timestamp) => {
      const date = new Date(timestamp * 1000);
      return date.toLocaleString();
    };

    const sendMessage = async () => {
      if (newMessage.value.trim() !== "") {
        loading.value = true;
        messages.value.push({
          sender: "You",
          text: newMessage.value,
          timestamp: getTimestamp(),
        });

        const userMessage = newMessage.value;
        newMessage.value = "";

        try {
          const response = await fetch(" http://127.0.0.1:5000/generate-answer", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ content: userMessage }),
          });

          if (response.ok) {
            const data = await response.json();
            messages.value.push({
              sender: "LLaMA",
              text: data.answer,
              timestamp: getTimestamp(),
            });
          } else {
            messages.value.push({
              sender: "Error",
              text: "Unable to generate an answer, please try again later.",
              timestamp: getTimestamp(),
            });
          }
        } catch (error) {
          messages.value.push({
            sender: "Error",
            text: "Unable to connect to the server, please check your network.",
            timestamp: getTimestamp(),
          });
        } finally {
          loading.value = false;
          await saveMessage();
          nextTick(() => {
            const chatBox = document.querySelector('.chat-box');
            chatBox.scrollTop = chatBox.scrollHeight;
          });
        }
      }
    };

    const saveMessage = async () => {
      try {
        await fetch(" http://127.0.0.1:5000/Save", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            id: uuid.value,
            messages: messages.value,
          }),
        });
      } catch (error) {
        console.error("Error saving message:", error);
      }
    };

    const loadChatData = async (id) => {
      loading.value = true;
      try {
        const response = await axios.get(` http://127.0.0.1:5000/chat/${id}`);
        messages.value = response.data.messages || [];
      } catch (error) {
        console.error("Error fetching file:", error);
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadChatData(uuid.value);
    });

    watch(
        () => route.params.uuid,
        (newUUID) => {
          uuid.value = newUUID;
          loadChatData(newUUID);
        }
    );

    return {
      newMessage,
      messages,
      sendMessage,
      formatTimestamp,
      loading,
    };
  },
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding: 20px;
  border: 1px solid #ddd;
}

.chat-box {
  flex: 1;
  padding: 10px;
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 5px;
  overflow-y: auto;
}

.message {
  display: flex;
  margin-bottom: 10px;
}

.user-message {
  justify-content: flex-end; /* User messages aligned to the right */
}

.bot-message {
  justify-content: flex-start; /* Bot messages aligned to the left */
}

.message-content {
  max-width: 60%;
  padding: 10px;
  background-color: #e9ecef;
  border-radius: 10px;
  word-wrap: break-word;
  box-sizing: border-box; /* Ensures padding does not affect width */
}

.user-message .message-content {
  background-color: #28a745;
  color: white;
  margin-left: auto; /* User message aligned to the right */
}

.bot-message .message-content {
  margin-right: 0; /* Ensures bot messages don't exceed left boundary */
}

.chat-input {
  display: flex;
  flex-direction: column;
  margin-top: 10px;
}

input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
}

button {
  margin-top: 10px;
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #218838;
}
</style>
