/*
  Warnings:

  - Added the required column `salt` to the `Login` table without a default value. This is not possible if the table is not empty.

*/
-- RedefineTables
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_Login" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "userId" INTEGER NOT NULL,
    "username" BLOB NOT NULL,
    "password" BLOB NOT NULL,
    "service" TEXT NOT NULL,
    "salt" BLOB NOT NULL,
    CONSTRAINT "Login_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);
INSERT INTO "new_Login" ("id", "password", "service", "userId", "username") SELECT "id", "password", "service", "userId", "username" FROM "Login";
DROP TABLE "Login";
ALTER TABLE "new_Login" RENAME TO "Login";
PRAGMA foreign_key_check;
PRAGMA foreign_keys=ON;
