<template>
  <div class="home-container">
    <!-- 侧边栏 -->
    <div class="sidebar-container">
      <SideBar :chats="chats" @chat-selected="selectChat" @add-new-chat="handleAddNewChat" @delete-chat="handleDeleteChat" />
    </div>

    <!-- 聊天区域 -->
    <div class="chat-area-container">
      <ChatArea :chatId="chatId" />
    </div>
  </div>
</template>

<script>
import SideBar from "@/components/SideBar.vue";
import ChatArea from "@/components/ChatArea.vue";
import { v4 as uuidv4 } from 'uuid';



export default {

  components: {
    SideBar,
    ChatArea
  },
  data() {
    return {
      chats: [], // 聊天列表
      chatId: null // 当前选中的聊天
    };
  },
  mounted() {
    // 初次加载时获取聊天记录
    this.fetchChats();
    this.interval = setInterval(this.fetchChats, 5000);
  },
  methods: {
    // 获取聊天记录
    fetchChats() {
      fetch('http://localhost:5000/Get_index', {
        method: "GET",
      })
          .then(response => {
            if (!response.ok) {
              throw new Error('网络响应不是 OK');
            }
            return response.json();
          })
          .then(data => {
            this.chats = data['chats'];
          })
          .catch(error => {
            console.error('发生错误:', error);
          });
    },

    // 处理选中聊天
    selectChat(chat) {
      this.chatId = chat;
    },

    // 处理添加新聊天
    handleAddNewChat() {
      const newChatId = uuidv4(); // 生成唯一的聊天 ID
      const newChat = {
        uuid: newChatId,
        name: `新聊天 ${this.chats.length + 1}`,
        timestamp: Math.floor(Date.now() / 1000)
      };

      // 添加新聊天到聊天列表
      this.chats.push(newChat);

      // 保存到后端
      this.saveNewChat(newChat);
    },

    // 保存新聊天记录到后端
    saveNewChat(newChat) {
      fetch('http://localhost:5000/Save', {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          id: newChat.uuid,
          messages: [{
            sender: "System",
            text: newChat.name,
            timestamp: newChat.timestamp
          }]
        })
      })
          .then(response => {
            if (!response.ok) {
              throw new Error('保存聊天记录失败');
            }
            return response.json();
          })
          .then(data => {
            console.log('聊天记录已保存:', data);
            // 刷新页面或重新获取聊天记录
            this.fetchChats();
          })
          .catch(error => {
            console.error('发生错误:', error);
          });
    },

    // 处理删除聊天
    handleDeleteChat(chatId) {
      // 调用后端删除聊天的接口
      fetch(`http://localhost:5000/DeleteChat?id=${chatId}`, {
        method: "DELETE"
      })
          .then(response => {
            if (!response.ok) {
              throw new Error('删除聊天失败');
            }
            return response.json();
          })
          .then(data => {
            console.log('聊天已删除:', data);
            // 从前端列表中移除聊天
            this.chats = this.chats.filter(chat => chat.uuid !== chatId);
            // 重置当前选中的聊天
            if (this.chatId === chatId) {
              this.chatId = null;
            }
          })
          .catch(error => {
            console.error('发生错误:', error);
          });
    }
  }
};
</script>

<style scoped>
.home-container {
  display: flex;
  height: 100vh;
}

.sidebar-container {
  width: 250px;
  background-color: #343a40;
  color: white;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.chat-area-container {
  flex-grow: 1;
  background-color: #f8f9fa;
  padding: 20px;
  display: flex;
  flex-direction: column;
}
</style>
