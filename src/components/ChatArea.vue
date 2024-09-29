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
import { ref, onMounted, nextTick, watch } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

export default {
  name: "ChatArea",

  setup() {
    const route = useRoute();
    const uuid = ref(route.params.uuid); // 使用 ref 包装 uuid
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
        newMessage.value = ""; // 清空输入框

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
            messages.value.push({
              sender: "LLaMA",
              text: data.question,
              timestamp: getTimestamp(),
            });
          } else {
            messages.value.push({
              sender: "Error",
              text: "无法生成问题，请稍后重试。",
              timestamp: getTimestamp(),
            });
          }
        } catch (error) {
          messages.value.push({
            sender: "Error",
            text: "无法连接到服务器，请检查网络。",
            timestamp: getTimestamp(),
          });
        } finally {
          loading.value = false; // 完成发送
          await saveMessage();
          nextTick(() => {
            const chatBox = document.querySelector('.chat-box');
            chatBox.scrollTop = chatBox.scrollHeight; // 滚动到最新消息
          });
        }
      }
    };

    const saveMessage = async () => {
      try {
        await fetch("http://localhost:5000/Save", {
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
        console.error("保存消息时出错:", error);
      }
    };

    const loadChatData = async (id) => {
      loading.value = true;
      try {
        const response = await axios.get(`http://localhost:5000/chat/${id}`); // 替换为您的 API 地址
        messages.value = response.data.messages || [];
      } catch (error) {
        console.error("获取文件时出错:", error);
      } finally {
        loading.value = false; // 完成加载
      }
    };

    onMounted(() => {
      loadChatData(uuid.value); // 组件挂载时加载数据
    });

    watch(
        () => route.params.uuid, // 侦听 UUID 的变化
        (newUUID) => {
          uuid.value = newUUID; // 更新 uuid
          loadChatData(newUUID); // 加载新的聊天内容
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
