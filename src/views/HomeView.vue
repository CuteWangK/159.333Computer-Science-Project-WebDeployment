<template>
  <div class="home-container">
    <!-- 侧边栏 -->
    <div class="sidebar-container">
      <SideBar :chats="chats" @chat-selected="selectChat" />
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

  methods: {
    selectChat(chat) {
      this.chatId = chat // 设置选中的聊天
    },
    async fetchChats(){
      try {
        const response = await fetch('http://localhost:5000/Get_index', {
          method: "GET" ,
        });
        if (!response.ok) {
          throw new Error('网络响应不是 OK');
        }
        const data = await response.json();
        this.chats = data['chats'];
        console.log('获取的数据:', data); // 监测原始数据
        this.chats = data.chats; // 更新聊天记录
      } catch (error) {
        console.error('发生错误:', error);
      }
    }
  },
  mounted() {
    this.fetchChats()
    if (this.chatId == null){
      this.chatId = uuidv4();
    }
    this.interval = setInterval(() => {
      this.fetchChats(); // 每0.5秒更新一次
    }, 500);
  }
};
</script>

<style scoped>
/* 使用 flexbox 实现布局 */
.home-container {
  display: flex;
  height: 100vh; /* 设置为占满屏幕高度 */
}

.sidebar-container {
  width: 250px; /* 侧边栏的固定宽度 */
  background-color: #343a40; /* 背景颜色，可以根据需要更改 */
  color: white;
  display: flex;
  flex-direction: column;
  height: 100vh; /* 确保侧边栏和页面高度一致 */
}

.chat-area-container {
  flex-grow: 1; /* 主内容区域占据剩余的宽度 */
  background-color: #f8f9fa; /* 主内容区域的背景颜色 */
  padding: 20px; /* 添加内边距 */
  display: flex;
  flex-direction: column;
}
</style>
