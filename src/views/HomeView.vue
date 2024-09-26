<template>
  <div class="home-container">
    <!-- 侧边栏 -->
    <div class="sidebar-container">
      <SideBar />
    </div>

    <!-- 聊天区域 -->
    <div class="chat-area-container">
      <ChatArea />
    </div>
  </div>
</template>

<script>
import SideBar from "@/components/SideBar.vue";
import ChatArea from "@/components/ChatArea.vue";

export default {
  name: "HomeView",
  components: {SideBar, ChatArea},
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
