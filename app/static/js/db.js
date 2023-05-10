const sqlite3 = require("sqlite3").verbose();

const db = new sqlite3.Database("../../data.db");

function search() {
    db.serialize(() => {
        db.each("SELECT rowid AS id, info FROM lorem", (err, row) => {
            console.log(row.id + ": " + row.info);
        });
    });
}

db.close();