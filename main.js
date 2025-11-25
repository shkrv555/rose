const express = require("express");
const path = require("path");
const fs = require("fs");
const multer = require("multer");

const app = express();
const PORT = 3000;
app.use(express.json());

const imageStorage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, path.join(__dirname, "fsdb", "images"));
    },
    filename: function (req, file, cb) {
        const ext = path.extname(file.originalname);
        const fileName = `${Date.now()}${ext}`;
        cb(null, fileName);
    }
});

const upload = multer({ storage: imageStorage });

if (!fs.existsSync(path.join(__dirname, "fsdb", "images"))) {
    fs.mkdirSync(path.join(__dirname, "fsdb", "images"), { recursive: true });
}

// Serve static files in /public
app.use(express.static(path.join(__dirname, "public")));

app.post("/upload-image", upload.single("image"), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ message: "No image uploaded" });
    }

    const imageUrl = `/images/${req.file.filename}`;

    res.json({
        message: "Image uploaded",
        url: imageUrl
    });
});

app.use("/images", express.static(path.join(__dirname, "fsdb", "images")));

// Route: /admin -> public/admin.html
app.get("/admin", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "admin.html"));
});

// Route: /menu -> public/menu.html
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "menu.html"));
});

app.post('/storage/:key', (req, res) => {
    const key = req.params.key;
    const value = req.body; // whole body is value

    fs.writeFile(
        path.join(__dirname, "fsdb", `${key}.json`),
        JSON.stringify(value, null, 2),
        err => {
            if (err) return res.status(500).json({ message: "Error saving key" });
            res.json({ message: `Saved key "${key}" successfully` });
        }
    );
});

app.get('/storage/:key', (req, res) => {
    const key = req.params.key;
    const filePath = path.join(__dirname + "/fsdb", `${key}.json`);

    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            if (err.code === 'ENOENT') return res.json(null); // Key not found
            return res.status(500).json({ message: "Error reading key" });
        }
        try {
            res.json(JSON.parse(data));
        } catch {
            res.status(500).json({ message: "Invalid JSON in file" });
        }
    });
});


app.listen(PORT, () => {
  console.log(`Server running: http://localhost:${PORT}`);
});
