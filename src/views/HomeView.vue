<template>
  <div class="home-container">
    <!-- Sidebar -->
    <div class="sidebar-container">
      <SideBar :chats="chats" @chat-selected="selectChat" @add-new-chat="handleAddNewChat" @delete-chat="handleDeleteChat" />
    </div>

    <!-- Chat Area -->
    <div class="chat-area-container">
      <!-- Display ChatArea only when a chat is selected -->
      <ChatArea v-if="chatId" :chatId="chatId" />
      <div v-else class="no-chat">Please select a chat or create a new chat</div>
    </div>
  </div>
</template>

<script>
import SideBar from "@/components/SideBar.vue";
import ChatArea from "@/components/ChatArea.vue";
import {v4 as uuidv4} from 'uuid'; // Import UUID generator

export default {
  components: {
    SideBar,
    ChatArea
  },
  data() {
    return {
      chats: [], // List of chats
      chatId: null // Currently selected chat
    };
  },
  props: ['uuid'], // Accept route parameters
  mounted() {
    // Fetch chat history on initial load
    this.fetchChats();
    // If a UUID is passed through the route, load the corresponding chat
    if (this.uuid) {
      this.chatId = this.uuid;
    }
  },
  watch: {
    '$route.params.uuid': function (newUuid) {
      this.chatId = newUuid;  // Update chatId when the route changes
    }
  },
  methods: {
    // Fetch chat history
    fetchChats() {
      fetch(' http://127.0.0.1:5000/Get_index', {
        method: "GET",
      })
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not OK');
            }
            return response.json();
          })
          .then(data => {
            this.chats = data['chats'];
          })
          .catch(error => {
            console.error('An error occurred:', error);
          });
    },

    // Handle selecting a chat
    selectChat(chat) {
      this.$router.push(`/chat/${chat}`); // Route navigation to the chat page
    },

    // Handle adding a new chat
    handleAddNewChat() {
      const newChatId = uuidv4(); // Generate a unique chat ID
      const newChat = {
        uuid: newChatId,
        name: `New Chat`,
        timestamp: Math.floor(Date.now() / 1000)
      };

      // Add the new chat to the chat list
      this.chats.push(newChat);

      // Save to the backend
      this.saveNewChat(newChat);
    },

    // Save new chat to the backend (without system messages)
    saveNewChat(newChat) {
      fetch('http://127.0.0.1:5000/Save', {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          id: newChat.uuid,
          messages: [] // No system messages, initialize with an empty chat history
        })
      })
          .then(response => {
            if (!response.ok) {
              throw new Error('Failed to save chat history');
            }
            return response.json();
          })
          .then(data => {
            console.log('Chat history saved:', data);
            // Refresh the page or refetch chat history
            this.fetchChats();
          })
          .catch(error => {
            console.error('An error occurred:', error);
          });
    },

    // Handle deleting a chat
    handleDeleteChat(chatId) {
      // Call backend to delete chat
      fetch(`http://127.0.0.1:5000/DeleteChat?id=${chatId}`, {
        method: "DELETE"
      })
          .then(response => {
            if (!response.ok) {
              throw new Error('Failed to delete chat');
            }
            return response.json();
          })
          .then(data => {
            console.log('Chat deleted:', data);
            // Remove the chat from the frontend list
            this.chats = this.chats.filter(chat => chat.uuid !== chatId);
            // Reset currently selected chat
            if (this.chatId === chatId) {
              this.chatId = null;
            }
          })
          .catch(error => {
            console.error('An error occurred:', error);
          });
    }
  }
};
</script>

<style scoped>
.home-container {
  width: 100%;
  display: flex;
  height: 100vh;
}

.sidebar-container {
  width: 12%;
  background-color: #343a40;
  color: white;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.chat-area-container {
  width: 88%;
  background-color: #f8f9fa;
  padding: 20px;
  padding-right: 0px;
  display: flex;
  flex-direction: column;
}

.no-chat {
  font-size: 1.2em;
  color: #888;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}
</style>
