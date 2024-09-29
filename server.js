const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5000;

// 中间件
app.use(cors());
app.use(bodyParser.json());

// 连接到 MongoDB
mongoose.connect('mongodb://localhost:27017/chat-app', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

// 聊天记录模型
const MessageSchema = new mongoose.Schema({
    text: String,
    timestamp: { type: Date, default: Date.now },
});

const Message = mongoose.model('Message', MessageSchema);

// POST 端点保存聊天记录
app.post('/api/messages', async (req, res) => {
    try {
        const newMessage = new Message({ text: req.body.text });
        await newMessage.save();
        res.status(201).json(newMessage);
    } catch (error) {
        res.status(500).json({ error: '保存消息时发生错误' });
    }
});

// 启动服务器
app.listen(PORT, () => {
    console.log(`服务器在 http://localhost:${PORT} 上运行`);
});
