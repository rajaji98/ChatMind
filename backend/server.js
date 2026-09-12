const express = require("express");
const cors = require("cors");
const { spawn } = require("child_process");
const path = require("path");

const app = express();

const PORT = 5000;

app.use(cors());
app.use(express.json());

// ============================================================
// SERVE FRONTEND
// ============================================================

const frontendPath = path.join(
    __dirname,
    "..",
    "frontend"
);

app.use(express.static(frontendPath));
console.log("Serving frontend from:", frontendPath);
// ============================================================
// HEALTH CHECK
// ============================================================

app.get("/api/health", (req, res) => {
    res.json({
        status: "ok",
        service: "ChatMind API"
    });
});

// ============================================================
// SEARCH
// ============================================================

app.post("/api/search", (req, res) => {

    const { query } = req.body;

    if (!query || !query.trim()) {
        return res.status(400).json({
            error: "Search query is required"
        });
    }

    const pythonScript = path.join(
        __dirname,
        "..",
        "scripts",
        "search_engine.py"
    );

    const python = spawn(
        "python",
        [
            pythonScript,
            query.trim(),
            "--json"
        ]
    );

    let output = "";
    let errorOutput = "";

    // ---------------------------------------------
    // Python stdout
    // ---------------------------------------------

    python.stdout.on("data", (data) => {
        output += data.toString();
    });

    // ---------------------------------------------
    // Python stderr
    // ---------------------------------------------

    python.stderr.on("data", (data) => {
        errorOutput += data.toString();
    });

    // ---------------------------------------------
    // Python finished
    // ---------------------------------------------

    python.on("close", (code) => {

        if (code !== 0) {

            console.error(
                "Python search error:",
                errorOutput
            );

            return res.status(500).json({
                error: "Search engine failed"
            });
        }

        try {

            const result = JSON.parse(output);

            res.json(result);

        } catch (error) {

            console.error(
                "Invalid JSON from search engine:"
            );

            console.error(output);

            return res.status(500).json({
                error: "Invalid response from search engine"
            });
        }

    });

    // ---------------------------------------------
    // Handle Python process errors
    // ---------------------------------------------

    python.on("error", (error) => {

        console.error(
            "Failed to start Python:",
            error
        );

        res.status(500).json({
            error: "Could not start search engine"
        });

    });

});

// ============================================================
// START SERVER
// ============================================================

app.listen(PORT, () => {

    console.log(
        `🚀 ChatMind API running on http://localhost:${PORT}`
    );

});