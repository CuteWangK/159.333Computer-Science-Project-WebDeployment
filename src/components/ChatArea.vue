<template>
  <div class="chat-container">

    <div class="chat-box">
      <div v-for="(message, index) in messages" :key="index" class="message">
        <strong>{{ message.sender }}({{ formatTimestamp(message.timestamp) }}):</strong> {{ message.text }}
      </div>
    </div>


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
      newMessages: [],
      loading :false
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
        this.loadChatData(`/data/${newPath}.json`);

    }
  },

  methods: {
    formatTimestamp(timestamp) {
      const date = new Date(timestamp * 1000);
      return date.toLocaleString();
    },
    loadChatData(path) {
      console.log(path);
      this.loading = true; // 开始加载
      this.error = null;   // 清除之前的错误信息

      // 读取 JSON 文件
      fetch(path)
          .then(response => {
            if (!response.ok) {
              throw new Error('无法加载聊天内容');
            }
            return response.json();
          })
          .then(data => {
            this.messages = data.messages; // 假设 messages 是 JSON 文件中的内容
          })
          .catch(err => {
            this.error = err.message; // 记录错误信息
            console.error('加载聊天数据时出错:', err);
          })
          .finally(() => {
            this.loading = false; // 完成加载
          });
    },
    async sendMessage() {

      this.newMessages = []
      if (this.newMessage.trim() !== "") {
        this.loading = true;
        this.messages.push({
          sender: "You",
          text: this.newMessage,
          timestamp: getTimestamp()
        });
        this.newMessages.push({
          sender: "You",
          text: this.newMessage,
          timestamp: getTimestamp()
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
            this.newMessages.push({
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
          this.loading = false; // 完成发送
            await this.saveMessage()
            this.$nextTick(() => {
            const chatBox = this.$el.querySelector('.chat-box');
            chatBox.scrollTop = chatBox.scrollHeight; // 滚动到最新消息
          })
        }
      }
    },
    async saveMessage() {
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
  margin-bottom: 10px;
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
