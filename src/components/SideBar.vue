<template>
  <div class="app-container">
    <!-- 侧边栏 -->
    <div class="sidebar">
      <h5 class="sidebar-title">Chat Sidebar</h5>
      <ul class="list-group">
        <li v-for="chat in sortedChats"
            :key="chat.timestamp"
            @click="handleChatClick(chat.uuid)"
            class="list-group-item">
          {{ chat.name }}({{formatTimestamp(chat.timestamp)}})</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {

  props: {
    chats: {
      type: Array,
      required: true
    }
  },
  computed: {
    sortedChats() {
      let thisChats = [];
      thisChats = this.chats
      return thisChats.sort((a, b) => b.timestamp - a.timestamp);
    }
  },
  methods: {
    formatTimestamp(timestamp) {
      const date = new Date(timestamp * 1000);
      return date.toLocaleString();
    },
    handleChatClick(chat) {
      this.$emit('chat-selected', chat);
    }
  }
};
</script>

<style scoped>
/* 布局容器 */
.app-container {
  display: flex;
  height: 100vh;
}

/* 侧边栏样式 */
.sidebar {
  width: 250px;
  background-color: #343a40;
  color: #fff;
  padding: 20px;
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  overflow-y: auto;
}

.sidebar-title {
  margin-bottom: 20px;
}

.list-group-item {
  cursor: pointer;
  background-color: #343a40;
  color: #fff;
  border: none;
  padding: 10px 15px;
}

.list-group-item:hover {
  background-color: #495057;
}

/* 主内容样式 */
.main-content {
  margin-left: 250px; /* 主页面内容要避免被侧边栏遮住 */
  padding: 20px;
  width: calc(100% - 250px);
  height: 100%;
  overflow-y: auto;
}

.chat-box {
  background-color: #f8f9fa;
  padding: 20px;
  height: 80%;
  overflow-y: scroll;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.chat-input {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
}
</style>
