const express = require("express");
const path = require("path");

const app = express();
const PORT = 3000;

// Serve static files in /public
app.use(express.static(path.join(__dirname, "public")));

// Route: /admin -> public/admin.html
app.get("/admin", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "admin.html"));
});

// Route: /menu -> public/menu.html
app.get("/menu", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "menu.html"));
});

app.get('/menu.json', (req, res) => {
    res.sendFile(path.join(__dirname, 'menu.json'));
});

app.post('/save-menu', (req, res) => {
    const menuData = req.body;

    fs.writeFile(
        path.join(__dirname, 'menu.json'),
        JSON.stringify(menuData, null, 2),
        err => {
            if (err) {
                console.error(err);
                return res.status(500).json({ message: "Error saving" });
            }
            res.json({ message: "Saved successfully" });
        }
    );
});


app.listen(PORT, () => {
  console.log(`Server running: http://localhost:${PORT}`);
});
