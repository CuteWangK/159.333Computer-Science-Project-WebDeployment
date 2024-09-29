<template>
  <div class="chat-container">
    <!-- 聊天显示区域 -->
    <div class="chat-box">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message', message.sender === 'You' ? 'message-right' : 'message-left']"
      >
        <div class="message-content">
          <strong>{{ message.sender }}:</strong> {{ message.text }} <small class="timestamp">({{ formatTimestamp(message.timestamp) }})</small>
        </div>
      </div>
    </div>

    <!-- 聊天输入区域 -->
    <div class="chat-input">
      <input
        v-model="newMessage"
        type="text"
        class="form-control"
        placeholder="请输入您的消息"
        @keyup.enter="sendMessage"
      />
      <button class="btn btn-success mt-2" @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script>
function getTimestamp() {
  return Math.floor(Date.now() / 1000);
}

export default {
  name: "ChatArea",

  data() {
    return {
      newMessage: "",
      messages: [],
      loading: false
    };
  },
  props: {
    chatId: {
      type: String,
      required: true
    }
  },
  watch: {
    chatId(newPath) {
    if (newPath) {
      // 确保路径有效才进行加载
      this.loadChatData(`/data/${newPath}.json`);
    }
  }
  },
  methods: {
    formatTimestamp(timestamp) {
      const date = new Date(timestamp * 1000);
      return date.toLocaleString();
    },
    loadChatData(path) {
      this.loading = true;
      this.error = null;
      fetch(path)
        .then(response => {
          if (!response.ok) {
            throw new Error('无法加载聊天内容');
          }
          return response.json();
        })
        .then(data => {
          this.messages = data.messages;
        })
        .catch(err => {
          this.error = err.message;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    async sendMessage() {
      if (this.newMessage.trim() !== "") {
        this.loading = true;
        const timestamp = getTimestamp();
        this.messages.push({
          sender: "You",
          text: this.newMessage,
          timestamp: timestamp
        });
        const userMessage = this.newMessage;
        this.newMessage = ""; // 清空输入框

        try {
          const response = await fetch("http://localhost:5000/generate-question", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ content: userMessage }),
          });

          if (response.ok) {
            const data = await response.json();
            this.messages.push({
              sender: "LLaMA",
              text: data.question,
              timestamp: getTimestamp()
            });
          } else {
            this.messages.push({
              sender: "Error",
              text: "无法生成问题，请稍后重试。",
              timestamp: getTimestamp()
            });
          }
        } catch (error) {
          this.messages.push({
            sender: "Error",
            text: "无法连接到服务器，请检查网络。",
            timestamp: getTimestamp()
          });
        } finally {
          this.loading = false;
          // 保存消息
          this.saveMessages();
          this.$nextTick(() => {
            const chatBox = this.$el.querySelector('.chat-box');
            chatBox.scrollTop = chatBox.scrollHeight; // 滚动到最新消息
          });
        }
      }
    },
    async saveMessages() {
      try {
        await fetch("http://localhost:5000/Save", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            id: this.chatId,
            messages: this.messages
          })
        });
      } catch (error) {
        console.error('保存消息时出错:', error);
      }
    }
  }
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
  display: flex;
  flex-direction: column;
}

.message {
  display: flex;
  max-width: 60%;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 10px;
  word-wrap: break-word;
}

.message-left {
  align-self: flex-start;
  background-color: #e9ecef;
}

.message-right {
  align-self: flex-end;
  background-color: #d4edda;
}

.message-content {
  white-space: pre-wrap;
  word-wrap: break-word;
}

.timestamp {
  color: #888;
  font-size: 0.8em;
  margin-left: 10px;
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
