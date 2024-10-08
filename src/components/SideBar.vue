<template>
  <div class="sidebar">
    <h5 class="sidebar-title">Chat Sidebar</h5>

    <!-- 添加新聊天按钮，固定大小，文字始终为 NEW CHAT -->
    <button class="btn btn-primary mb-3 fixed-size-btn" @click="addNewChat">NEW CHAT</button>

    <ul class="list-group">
      <li v-for="chat in sortedChats" :key="chat.uuid" class="list-group-item">
        <div class="d-flex justify-content-between">
          <!-- 点击聊天记录时触发 handleChatClick -->
          <span @click="handleChatClick(chat.uuid)">
            {{ chat.name }} ({{ formatTimestamp(chat.timestamp) }})
          </span>
          <!-- 删除聊天 -->
          <button class="btn btn-danger btn-sm" @click="deleteChat(chat.uuid)">Delete</button>
        </div>
      </li>
    </ul>
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
      // 按时间戳降序排列聊天记录
      // eslint-disable-next-line vue/no-mutating-props,vue/no-side-effects-in-computed-properties
      return this.chats.sort((a, b) => b.timestamp - a.timestamp);
    }
  },
  methods: {
    formatTimestamp(timestamp) {
      const date = new Date(timestamp * 1000);
      return date.toLocaleString();
    },
    handleChatClick(chatId) {
      // 触发父组件的路由导航
      this.$emit('chat-selected', chatId);
    },
    addNewChat() {
      // 触发父组件添加新聊天事件
      this.$emit('add-new-chat');
    },
    deleteChat(chatId) {
      // 触发父组件删除聊天事件
      this.$emit('delete-chat', chatId);
    }
  }
};
</script>

<style scoped>
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

.fixed-size-btn {
  width: 150px; /* 固定宽度 */
  height: 40px; /* 固定高度 */
  white-space: nowrap; /* 禁止换行 */
  overflow: hidden; /* 超出部分隐藏 */
  text-overflow: ellipsis; /* 溢出部分使用省略号 */
  display: inline-block;
}

.list-group-item {
  cursor: pointer;
  background-color: #343a40;
  color: #fff;
  border: none;
  padding: 10px 15px;
  min-height: 50px; /* 设置最小高度 */
  display: flex; /* 使用 Flexbox 布局 */
  justify-content: space-between; /* 分隔元素 */
  align-items: center; /* 垂直居中对齐 */
}

.list-group-item:hover {
  background-color: #495057;
}

.d-flex {
  display: flex;
  justify-content: space-between;
}
</style>
