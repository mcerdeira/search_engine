const DBSOURCE = "../../data/crawled_web.db";
let sqlite3 = require('sqlite3').verbose();
let db = new sqlite3.Database(DBSOURCE);

let GetData = function (queryString, retFunc) {
    let sql = "select title,url from result where title like '%' || ? || '%' limit 100";
    let params = [queryString];
    db.all(sql, params, (err, rows) => {
        if (err) {
            retFunc([{ "error": err.message }]);
        }
        retFunc(rows);
    });
}

module.exports.GetData = GetData;