const fs = require("fs");
const path = require("path");

const messagesPath = path.join(
    __dirname,
    "data",
    "messages.json"
);

const messages = JSON.parse(
    fs.readFileSync(messagesPath, "utf-8")
);


/*
    We will initially use a simple Python-powered
    semantic search service.

    This JS file handles:
    - loading messages
    - formatting results
    - conversation context
*/


function getContext(index, radius = 2) {
    const start = Math.max(0, index - radius);
    const end = Math.min(messages.length, index + radius + 1);

    return messages.slice(start, end);
}


function formatResult(index, similarity) {
    const message = messages[index];

    return {
        id: message.id,
        sender: message.sender,
        timestamp: message.timestamp,
        text: message.text,
        similarity: Number(similarity.toFixed(4)),
        context: getContext(index)
    };
}


function getMessageByIndex(index) {
    if (index < 0 || index >= messages.length) {
        return null;
    }

    return messages[index];
}


module.exports = {
    messages,
    getContext,
    formatResult,
    getMessageByIndex
};