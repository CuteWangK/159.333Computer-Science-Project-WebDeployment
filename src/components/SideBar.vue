<template>
  <div class="sidebar">
    <h5 class="sidebar-title">Chat Sidebar</h5>

    <!-- Add a new chat button with fixed size, always displaying NEW CHAT -->
    <button class="btn btn-primary mb-3 fixed-size-btn" @click="addNewChat">NEW CHAT</button>

    <ul class="list-group">
      <li v-for="chat in sortedChats" :key="chat.uuid" class="list-group-item">
        <div class="d-flex justify-content-between">
          <!-- Trigger handleChatClick when clicking on a chat record -->
          <span @click="handleChatClick(chat.uuid)">
            {{ chat.name }} ({{ formatTimestamp(chat.timestamp) }})
          </span>
          <!-- Delete chat -->
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
      // Sort chat records in descending order by timestamp
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
      // Trigger parent component's route navigation
      this.$emit('chat-selected', chatId);
    },
    addNewChat() {
      // Trigger parent component's add new chat event
      this.$emit('add-new-chat');
    },
    deleteChat(chatId) {
      // Trigger parent component's delete chat event
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
  width: 150px; /* Fixed width */
  height: 40px; /* Fixed height */
  white-space: nowrap; /* Prevent line breaks */
  overflow: hidden; /* Hide overflow */
  text-overflow: ellipsis; /* Show ellipsis for overflow */
  display: inline-block;
}

.list-group-item {
  cursor: pointer;
  background-color: #343a40;
  color: #fff;
  border: none;
  padding: 10px 15px;
  min-height: 50px; /* Set minimum height */
  display: flex; /* Use Flexbox layout */
  justify-content: space-between; /* Space elements apart */
  align-items: center; /* Vertically align items */
}

.list-group-item:hover {
  background-color: #495057;
}

.d-flex {
  display: flex;
  justify-content: space-between;
}
</style>
