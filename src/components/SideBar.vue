<template>
  <div class="sidebar">
    <h5 class="sidebar-title">Chat Sidebar</h5>

    <!-- 添加新聊天按钮 -->
    <button class="btn btn-primary mb-3" @click="addNewChat">NEW CHAT</button>

    <ul class="list-group">
      <li v-for="chat in sortedChats" :key="chat.uuid" class="list-group-item">
        <div class="d-flex justify-content-between">
          <span @click="handleChatClick(chat.uuid)">
            {{ chat.name }} ({{ formatTimestamp(chat.timestamp) }})
          </span>
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
      // eslint-disable-next-line vue/no-mutating-props,vue/no-side-effects-in-computed-properties
      return this.chats.sort((a, b) => b.timestamp - a.timestamp);
    }
  },
  methods: {
    formatTimestamp(timestamp) {
      const date = new Date(timestamp * 1000);
      return date.toLocaleString();
    },
    handleChatClick(chat) {
      this.$emit('chat-selected', chat);
    },
    addNewChat() {
      this.$emit('add-new-chat');
    },
    deleteChat(chatId) {
      // 触发父组件事件，传递需要删除的聊天 ID
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

.d-flex {
  display: flex;
  justify-content: space-between;
}

</style>
