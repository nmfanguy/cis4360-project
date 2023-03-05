/*
  Warnings:

  - You are about to alter the column `username` on the `Login` table. The data in that column could be lost. The data in that column will be cast from `String` to `Binary`.

*/
-- RedefineTables
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_Login" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "userId" INTEGER NOT NULL,
    "username" BLOB NOT NULL,
    "password" BLOB NOT NULL,
    "service" TEXT NOT NULL,
    CONSTRAINT "Login_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);
INSERT INTO "new_Login" ("id", "password", "service", "userId", "username") SELECT "id", "password", "service", "userId", "username" FROM "Login";
DROP TABLE "Login";
ALTER TABLE "new_Login" RENAME TO "Login";
PRAGMA foreign_key_check;
PRAGMA foreign_keys=ON;
