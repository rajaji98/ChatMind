const API_URL = "http://localhost:5000";

const searchInput = document.getElementById("searchInput");
const searchButton = document.getElementById("searchButton");
const resultsContainer = document.getElementById("resultsContainer");
const resultCount = document.getElementById("resultCount");
const searchStatus = document.getElementById("searchStatus");


// ============================================================
// SEARCH
// ============================================================

async function searchMessages(query) {

    query = query.trim();

    if (!query) {
        return;
    }

    searchButton.disabled = true;

    searchStatus.textContent = "Searching...";

    resultsContainer.innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">🧠</div>
            <h2>Finding relevant messages...</h2>
            <p>
                Searching across the conversation using semantic
                understanding.
            </p>
        </div>
    `;

    try {

        const response = await fetch(
            `${API_URL}/api/search`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    query: query
                })
            }
        );

        if (!response.ok) {
            throw new Error("Search request failed");
        }

        const data = await response.json();

        renderResults(data.results || []);

    } catch (error) {

        console.error(error);

        resultCount.textContent = "Search failed";

        searchStatus.textContent = "";

        resultsContainer.innerHTML = `
            <div class="error">
                ❌ Unable to connect to ChatMind API.
                <br><br>
                Make sure the backend is running on
                <strong>localhost:5000</strong>.
            </div>
        `;

    } finally {

        searchButton.disabled = false;

        searchStatus.textContent = "";

    }

}


// ============================================================
// RENDER RESULTS
// ============================================================

function renderResults(results) {

    if (!results.length) {

        resultCount.textContent = "No results found";

        resultsContainer.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">🔎</div>
                <h2>No matching messages</h2>
                <p>
                    Try asking the question in a different way.
                </p>
            </div>
        `;

        return;
    }


    resultCount.textContent =
        `${results.length} relevant messages`;


    resultsContainer.innerHTML =
        results.map(renderResult).join("");

}


// ============================================================
// RESULT CARD
// ============================================================

function renderResult(result) {

    const initials =
        result.sender
            .split(" ")
            .map(word => word[0])
            .join("")
            .slice(0, 2)
            .toUpperCase();


    const date =
        formatDate(result.timestamp);


    const messageType =
        formatMessageType(result.message_type);


    const context =
        (result.context || [])
            .map(message => `
                <div class="context-message">
                    <strong>${escapeHTML(message.sender)}</strong>
                    ${escapeHTML(message.text)}
                </div>
            `)
            .join("");


    return `
        <article class="result-card">

            <div class="result-top">

                <div class="sender">

                    <div class="avatar">
                        ${initials}
                    </div>

                    <div>

                        <div class="sender-name">
                            ${escapeHTML(result.sender)}
                        </div>

                        <div class="timestamp">
                            ${date}
                        </div>

                    </div>

                </div>

                <div class="score">
                    relevance ${result.rerank_score}
                </div>

            </div>


            <div class="message-text">
                ${escapeHTML(result.text)}
            </div>


            <div class="tags">

                <span class="tag decision">
                    ${messageType}
                </span>

                ${
                    result.topic
                    ? `
                        <span class="tag">
                            #${escapeHTML(result.topic)}
                        </span>
                    `
                    : ""
                }

                ${
                    result.thread_id
                    ? `
                        <span class="tag">
                            ${escapeHTML(
                                result.thread_id
                            )}
                        </span>
                    `
                    : ""
                }

            </div>


            ${
                context
                ? `
                    <div class="context-title">
                        Conversation context
                    </div>

                    <div class="context">
                        ${context}
                    </div>
                `
                : ""
            }

        </article>
    `;
}


// ============================================================
// HELPERS
// ============================================================

function formatDate(timestamp) {

    if (!timestamp) {
        return "";
    }

    const date = new Date(timestamp);

    return date.toLocaleString(
        "en-IN",
        {
            month: "short",
            day: "numeric",
            hour: "numeric",
            minute: "2-digit"
        }
    );
}


function formatMessageType(type) {

    if (!type) {
        return "Message";
    }

    return type
        .replaceAll("_", " ")
        .replace(/\b\w/g, char => char.toUpperCase());
}


function escapeHTML(value) {

    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


// ============================================================
// SEARCH BUTTON
// ============================================================

searchButton.addEventListener(
    "click",
    () => {
        searchMessages(searchInput.value);
    }
);


// ============================================================
// ENTER KEY
// ============================================================

searchInput.addEventListener(
    "keydown",
    event => {

        if (event.key === "Enter") {
            searchMessages(searchInput.value);
        }

    }
);


// ============================================================
// EXAMPLE QUERIES
// ============================================================

document
    .querySelectorAll(".example")
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                searchInput.value =
                    button.textContent.trim();

                searchMessages(
                    searchInput.value
                );

            }
        );

    });