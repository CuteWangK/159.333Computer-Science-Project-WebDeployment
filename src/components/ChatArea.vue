<template>
  <div class="chat-container">
    <!-- 聊天显示区域 -->
    <div class="chat-box">
      <div v-for="(message, index) in messages" :key="index" class="message">
        <strong>{{ message.sender }}:</strong> {{ message.text }}
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
export default {
  name: "ChatArea",
  data() {
    return {
      newMessage: "", // 输入的新消息
      messages: [], // 消息记录
    };
  },
  methods: {
    // 发送消息
    sendMessage() {
      if (this.newMessage.trim() !== "") {
        // 推送新消息到消息数组
        this.messages.push({
          sender: "You",
          text: this.newMessage,
        });
        // 清空输入框
        this.newMessage = "";
      }
    },
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
