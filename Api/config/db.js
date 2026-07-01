import mysql from 'mysql2/promise';

export const pool = mysql.createPool({
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'root',
    port: process.env.DB_PORT || 3333,
    password: process.env.DB_PASSWORD || 'root',
    database: process.env.DB_NAME || "clinique2nuitsv2",
    waitForConnections: true,
    connectionLimit: 10
});