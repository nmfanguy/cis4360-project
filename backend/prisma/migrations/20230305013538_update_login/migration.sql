/*
  Warnings:

  - Added the required column `password` to the `Login` table without a default value. This is not possible if the table is not empty.
  - Added the required column `service` to the `Login` table without a default value. This is not possible if the table is not empty.
  - Added the required column `username` to the `Login` table without a default value. This is not possible if the table is not empty.

*/
-- RedefineTables
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_Login" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "userId" INTEGER NOT NULL,
    "username" TEXT NOT NULL,
    "password" BLOB NOT NULL,
    "service" TEXT NOT NULL,
    CONSTRAINT "Login_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);
INSERT INTO "new_Login" ("id", "userId") SELECT "id", "userId" FROM "Login";
DROP TABLE "Login";
ALTER TABLE "new_Login" RENAME TO "Login";
PRAGMA foreign_key_check;
PRAGMA foreign_keys=ON;
