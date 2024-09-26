<template>
  <div class="home-container">
    <!-- 侧边栏 -->
    <div class="sidebar-container">
      <SideBar :chats="chats" @chat-selected="selectChat" />
    </div>

    <!-- 聊天区域 -->
    <div class="chat-area-container">
      <ChatArea :chatFilePath="chatFilePath" />
    </div>
  </div>
</template>

<script>
import SideBar from "@/components/SideBar.vue";
import ChatArea from "@/components/ChatArea.vue";

export default {
  components: {
    SideBar,
    ChatArea
  },
  data() {
    return {
      chats: [], // 聊天列表
      chatFilePath: null // 当前选中的聊天
    };
  },
  mounted() {
    // 从JSON文件加载聊天数据
    fetch('/data/chats.json')
        .then(response => {
          if (!response.ok) {
            throw new Error('网络响应错误');
          }
          return response.json();
        })
        .then(data => {
          this.chats = data; // 将获取的数据赋值给 chats 数组
        })
        .catch(error => {
          console.error('获取聊天数据时出错:', error); // 处理任何错误
        });
  },
  methods: {
    selectChat(chat) {
      this.chatFilePath = `/data/chat${chat}.json` // 设置选中的聊天
    }
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
